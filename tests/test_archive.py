from pathlib import Path
from unittest import mock
from subprocess import CalledProcessError

import pytest

from noirnet.archive import Archiver
from noirnet.exceptions import MissingDependency


class TestArchive:
    @mock.patch("noirnet.archive.run")
    def test_preflight_check_detects_missing_dependency(self, mock_run):
        def fake_check_returncode():
            raise CalledProcessError(cmd="fake", returncode=1)

        mock_run.return_value.check_returncode.side_effect = fake_check_returncode

        with pytest.raises(MissingDependency) as excinfo:
            Archiver.preflight_check()
        expected_description = "Unable to locate tar utility"
        assert excinfo.value.args[0] == expected_description

    @mock.patch("noirnet.archive.chmod")
    @mock.patch("noirnet.archive.run")
    def test_create_archive_invokes_tar(self, mock_run, mock_chmod):
        source_dir = "/fake/path"
        source_file = "source"
        dest_path = "/fake/path/dest.tar.gz"
        source = Path(f"{source_dir}/{source_file}")
        dest = Path(dest_path)

        Archiver.create_archive(source, dest)
        mock_run.assert_called_once_with(
            ["tar", "czf", dest_path, "--directory", source_dir, source_file]
        )

    @mock.patch("noirnet.archive.run")
    def test_extract_archive_invokes_tar(self, mock_run):
        source_path = "/fake/path/source"
        source = Path(source_path)

        Archiver.extract_archive(source)
        mock_run.assert_called_once_with(["tar", "xzf", source_path])
