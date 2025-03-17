from os import chmod
from pathlib import Path
from subprocess import run, CalledProcessError

from noirnet.exceptions import MissingDependency


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
    def create_archive(source: Path, dest: Path):
        """Creates an archive of `source` at `dest`

        Arguments:
        source -- `Path` to source file or folder
        dest -- `Path` to destination file or folder
        """
        # tar doesn't accept the source file as a path.
        # instead, have to specify source directory
        # using --directory and then give the source
        # file name as a (positional) argument
        run(
            [
                "tar",
                "czf",
                dest.as_posix(),
                "--directory",
                source.parent.as_posix(),
                source.name,
            ]
        )
        chmod(dest, 0o700)

    @staticmethod
    def extract_archive(source: Path):
        run(["tar", "xzf", source.as_posix()])
