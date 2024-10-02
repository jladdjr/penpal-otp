from pathlib import Path
from unittest import mock

import pytest

from penpal.encrypt import Encrypter


class TestEncrypter:
    def test_preflight_check_raises_exception_for_missing_pad(self):
        encrypter = Encrypter()

        fake_pad_path = "/not/a/real.pad"
        fake_pad_path_obj = Path(fake_pad_path)

        mock_file_path = mock.MagicMock()
        mock_encrypted_file_path = mock.MagicMock()

        with pytest.raises(ValueError) as excinfo:
            encrypter.preflight_check(fake_pad_path_obj, mock_file_path,
                                      mock_encrypted_file_path)
        expected_description = ("Could not find one-time pad at " +
                                f"{fake_pad_path}")
        assert excinfo.value.args[0] == expected_description

    def test_preflight_check_raises_exception_for_missing_file(self):
        encrypter = Encrypter()

        mock_pad_path = mock.MagicMock()

        fake_file_path = "/not/a/real/file"
        fake_file_path_obj = Path(fake_file_path)

        mock_encrypted_file_path = mock.MagicMock()

        with pytest.raises(ValueError) as excinfo:
            encrypter.preflight_check(mock_pad_path, fake_file_path_obj,
                                      mock_encrypted_file_path)
        expected_description = ("Could not find file at " +
                                f"{fake_file_path}")
        assert excinfo.value.args[0] == expected_description

    @mock.patch("penpal.encrypt.Archiver")
    @mock.patch("penpal.encrypt.assert_secure_dir")
    def test_preflight_check_checks_pad_dir_and_archiver_pre_checks(self, mock_assert_secure_dir,
                                                                    mock_archiver):
        mock_pad_path = mock.MagicMock()
        mock_file_path = mock.MagicMock()
        mock_encrypted_file_path = mock.MagicMock()

        Encrypter.preflight_check(mock_pad_path, mock_file_path, mock_encrypted_file_path)

        mock_assert_secure_dir.assert_called_once_with(mock_pad_path)
        mock_archiver.preflight_check.assert_called_once()
