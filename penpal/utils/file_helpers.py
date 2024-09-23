from pathlib import Path
from stat import (S_IRUSR, S_IWUSR, S_IXUSR,
                  S_IRGRP, S_IWGRP, S_IXGRP,
                  S_IROTH, S_IWOTH, S_IXOTH)

from penpal.exceptions import PermissionException


def get_user_permissions(path: Path) -> (bool, bool, bool):
    """Returns the user-level permissions for a file as a tuple
    of three bools. The tuple gives the read, write, and execute
    permissions of the file (in that order).

    Arguments:
    path -- path to file
    """
    mode = path.stat().st_mode
    read = mode & S_IRUSR != 0
    write = mode & S_IWUSR != 0
    execute = mode & S_IXUSR != 0
    return (read, write, execute)


def get_group_permissions(path: Path) -> (bool, bool, bool):
    """Returns the group-level permissions for a file as a tuple
    of three bools. The tuple gives the read, write, and execute
    permissions of the file (in that order).

    Arguments:
    path -- path to file
    """
    mode = path.stat().st_mode
    read = mode & S_IRGRP != 0
    write = mode & S_IWGRP != 0
    execute = mode & S_IXGRP != 0
    return (read, write, execute)


def get_world_permissions(path: Path) -> (bool, bool, bool):
    """Returns the world-level permissions for a file as a tuple
    of three bools. The tuple gives the read, write, and execute
    permissions of the file (in that order).

    Arguments:
    path -- path to file
    """
    mode = path.stat().st_mode
    read = mode & S_IROTH != 0
    write = mode & S_IWOTH != 0
    execute = mode & S_IXOTH != 0
    return (read, write, execute)


def assert_secure_dir(path: Path):
    """Ensures that `path` is a directory with file permissions set to 700.
    Raises a `ValueError` if these conditions are not met.
    """
    if not path.exists():
        raise ValueError(f"{path} does not exist")
    if not path.is_dir():
        raise ValueError(f"{path} is not a directory")
    if get_user_permissions(path) != (True, True, True) or \
       get_group_permissions(path) != (False, False, False) or \
       get_world_permissions(path) != (False, False, False):
        raise PermissionException(f"{path} must have permissions set to 700")
