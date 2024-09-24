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
