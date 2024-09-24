from pathlib import Path
from unittest.mock import MagicMock

import pytest

from penpal.encrypt import Encrypter


class TestEncrypter:
    def test_preflight_check_raises_exception_for_missing_pad(self):
        encrypter = Encrypter()

        fake_pad_path = "/not/a/real.pad"
        fake_pad_path_obj = Path(fake_pad_path)

        mock_file_path = MagicMock()
        mock_encrypted_file_path = MagicMock()

        with pytest.raises(ValueError) as excinfo:
            encrypter.preflight_check(fake_pad_path_obj, mock_file_path,
                                      mock_encrypted_file_path)
        expected_description = ("Could not find one-time pad at " +
                                f"{fake_pad_path}")
        assert excinfo.value.args[0] == expected_description

    def test_preflight_check_raises_exception_for_missing_file(self):
        encrypter = Encrypter()

        mock_pad_path = MagicMock()

        fake_file_path = "/not/a/real/file"
        fake_file_path_obj = Path(fake_file_path)

        mock_encrypted_file_path = MagicMock()

        with pytest.raises(ValueError) as excinfo:
            encrypter.preflight_check(mock_pad_path, fake_file_path_obj,
                                      mock_encrypted_file_path)
        expected_description = ("Could not find file at " +
                                f"{fake_file_path}")
        assert excinfo.value.args[0] == expected_description
