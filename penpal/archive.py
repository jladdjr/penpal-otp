from os import chmod
from pathlib import Path
from subprocess import run, CalledProcessError

from penpal.exceptions import MissingDependency


class Archiver:
    @staticmethod
    def preflight_check():
        """Determine if archive utility is installed"""
        try:
            res = run(["tar", "--help"])
            res.check_returncode()
        except CalledProcessError:
            raise MissingDependency("Unable to locate tar utility")

    @staticmethod
    def create_archive(source_file: Path, dest_file: Path):
        run(["tar", "czf", dest_file.as_posix(),
             "-C", source_file.parent.as_posix(),
             source_file.name])
        chmod(dest_file, 0o700)
