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
    def create_archive(source_files: list[Path], dest_file: Path):
        # TODO: assumes all files are in the same directory
        source_file_names = [source_file.name
                             for source_file in source_files]
        run(["tar", "czf", dest_file.as_posix(),
             "-C", source_files[0].parent.as_posix(),
             *source_file_names])
        chmod(dest_file, 0o700)
