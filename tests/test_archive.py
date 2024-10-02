from unittest import mock
from subprocess import CalledProcessError

import pytest

from penpal.archive import Archiver
from penpal.exceptions import MissingDependency


class TestArchive:

    @mock.patch("penpal.archive.run")
    def test_preflight_check_detects_missing_dependency(self, mock_run):
        def fake_check_returncode():
            raise CalledProcessError(cmd="fake", returncode=1)
        mock_run.return_value.check_returncode.side_effect = fake_check_returncode

        with pytest.raises(MissingDependency) as excinfo:
            Archiver.preflight_check()
        expected_description = "Unable to locate tar utility"
        assert excinfo.value.args[0] == expected_description
