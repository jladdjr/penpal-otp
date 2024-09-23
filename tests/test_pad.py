from os import chmod
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import pytest

from penpal import pad
from penpal.settings import MAX_BLOCK_SIZE


class TestPad:
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

    def test_pad_created_at_path(self):
        """Ensure that `create_pad` creates a well-formed pad at a
        given directory
        """
        pass
