from math import ceil
from os import chmod
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import mock

import pytest

from penpal import pad
from penpal.settings import MAX_BLOCK_SIZE, STD_BLOCK_SIZE
from penpal.utils.file_helpers import assert_secure_dir


class TestCreateOneTimePad:
    def test_create_one_time_pad_fails_if_path_parent_dir_does_not_exist(self):
        path_missing_parent_folder = Path("/not-a-real-folder/my.pad")
        with pytest.raises(ValueError) as excinfo:
            pad.create_one_time_pad(path_missing_parent_folder, 100)
        expected_description = ("Cannot create one-time pad at " +
                                "/not-a-real-folder/my.pad; " +
                                "parent directory does not exist")
        assert excinfo.value.args[0] == expected_description

    @mock.patch("penpal.pad.create_block_file")
    @mock.patch("penpal.pad.os")
    @mock.patch("penpal.pad.assert_secure_dir")
    def test_create_one_time_pad_rejects_unsafe_parent_directory(self, mock_assert_secure_dir,
                                                                 mock_os,
                                                                 mock_create_block_file):
        """Ensure that `create_one_time_pad` calls `assert_secure_dir`
        to ensure that parent path is a directory with the appropriate
        access settings.
        """
        mock_path = mock.MagicMock()
        mock_path.parent.exists.return_value = True
        mock_path.exists.return_value = False

        pad.create_one_time_pad(mock_path, 100)

        mock_assert_secure_dir.assert_called_with(mock_path.parent)

    def test_create_one_time_pad_fails_if_path_already_exists(self):
        with TemporaryDirectory() as tmp_dir:
            with pytest.raises(ValueError) as excinfo:
                pad.create_one_time_pad(Path(tmp_dir), 100)
            expected_description = ("Cannot create one-time pad at " +
                                    f"{tmp_dir}; file or directory " +
                                    "already present at location")
            assert excinfo.value.args[0] == expected_description

        with NamedTemporaryFile() as tmp_file:
            with pytest.raises(ValueError) as excinfo:
                pad.create_one_time_pad(Path(tmp_file.name), 100)
            expected_description = ("Cannot create one-time pad at " +
                                    f"{tmp_file.name}; file or directory " +
                                    "already present at location")
            assert excinfo.value.args[0] == expected_description

    def test_create_one_time_pad_creates_dir_with_700_perms(self):
        with TemporaryDirectory() as tmp_dir:
            chmod(tmp_dir, 0o700)
            new_dir = Path(tmp_dir).joinpath("foo.pad")
            pad.create_one_time_pad(new_dir, 100)
            assert_secure_dir(new_dir)

    @mock.patch("penpal.pad.create_block_file")
    def test_create_one_time_pad_creates_correct_number_of_blocks(self, mock_create_block_file):
        pad_size = 10**6
        with TemporaryDirectory() as tmp_dir:
            chmod(tmp_dir, 0o700)
            new_dir = Path(tmp_dir).joinpath("foo.pad")
            pad.create_one_time_pad(new_dir, pad_size)
            calls = mock_create_block_file.mock_calls
            assert len(calls) == ceil(pad_size / STD_BLOCK_SIZE)
            for call in calls:
                assert call.args == (new_dir, STD_BLOCK_SIZE)


class TestCreateBlockFile:
    def test_create_block_file_refuses_to_create_huge_block(self):
        """Ensure that `create_block_file` requires the `size`
        be less than MAX_BLOCK_SIZE bytes.
        """
        bad_size = MAX_BLOCK_SIZE + 1
        with TemporaryDirectory() as tmp_dir:
            chmod(tmp_dir, 0o700)
            with pytest.raises(ValueError) as excinfo:
                pad.create_block_file(Path(tmp_dir), bad_size)
            expected_description = ("Cannot create blocks larger than "
                                    f"{MAX_BLOCK_SIZE} bytes. Received request "
                                    f"for {bad_size} bytes.")
            assert excinfo.value.args[0] == expected_description

    @mock.patch("penpal.pad.open")
    @mock.patch("penpal.pad.sha3_256")
    @mock.patch("penpal.pad.get_random_bytes")
    @mock.patch("penpal.pad.assert_secure_dir")
    def test_create_block_file_rejects_unsafe_directory(self, mock_assert_secure_dir,
                                                        mock_get_random_bytes,
                                                        mock_sha3_256,
                                                        mock_open):
        """Ensure that `create_block_file` calls `assert_secure_dir`
        to ensure that path is a directory with the appropriate access
        settings.
        """
        mock_path = mock.MagicMock()
        pad.create_block_file(mock_path, 100)
        mock_assert_secure_dir.assert_called()

    @mock.patch("penpal.pad.os")
    @mock.patch("penpal.pad.open")
    @mock.patch("penpal.pad.sha3_256")
    @mock.patch("penpal.pad.get_random_bytes")
    @mock.patch("penpal.pad.assert_secure_dir")
    def test_create_block_file_creates_block_file_at_path(self, mock_assert_secure_dir,
                                                          mock_get_random_bytes,
                                                          mock_sha3_256,
                                                          mock_open,
                                                          mock_os):
        """Ensure that `create_block_file` creates a block file at `path`"""
        fake_sha = 'fabbafcab'
        fake_full_path = f"/tmp/pads/foo.pad/{fake_sha}"
        fake_full_path_obj = Path(fake_full_path)

        mock_path = mock.MagicMock()
        mock_path.joinpath.return_value = fake_full_path_obj

        mock_sha3_256.return_value.hexdigest.return_value = fake_sha

        pad.create_block_file(mock_path, 100)

        mock_path.joinpath.assert_called_once_with(fake_sha)

        mock_open_calls = mock_open.return_value.__enter__.return_value.mock_calls
        assert len(mock_open_calls) == 1
        mock_open_calls[0].args[0].as_posix() == fake_full_path

        mock_os.chmod.assert_called_once_with(fake_full_path_obj, 0o400)
