import os
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from penpal.exceptions import PermissionException
from penpal.utils import file_helpers


@pytest.mark.parametrize("chmod_mask,read,write,execute",
                         [[0o000, False, False, False],
                          [0o100, False, False, True],
                          [0o200, False, True, False],
                          [0o300, False, True, True],
                          [0o400, True, False, False],
                          [0o500, True, False, True],
                          [0o600, True, True, False],
                          [0o700, True, True, True],
                          [0o000, False, False, False],
                          [0o010, False, False, False],
                          [0o020, False, False, False],
                          [0o030, False, False, False],
                          [0o040, False, False, False],
                          [0o050, False, False, False],
                          [0o060, False, False, False],
                          [0o070, False, False, False],
                          [0o000, False, False, False],
                          [0o001, False, False, False],
                          [0o002, False, False, False],
                          [0o003, False, False, False],
                          [0o004, False, False, False],
                          [0o005, False, False, False],
                          [0o006, False, False, False],
                          [0o007, False, False, False],
                          [0o777, True, True, True]])
def test_get_user_permissions(chmod_mask, read, write, execute):
    with NamedTemporaryFile() as tmp_file:
        os.chmod(tmp_file.name, chmod_mask)
        path = Path(tmp_file.name)
        assert file_helpers.get_user_permissions(path) == (read, write, execute)


@pytest.mark.parametrize("chmod_mask,read,write,execute",
                         [[0o000, False, False, False],
                          [0o100, False, False, False],
                          [0o200, False, False, False],
                          [0o300, False, False, False],
                          [0o400, False, False, False],
                          [0o500, False, False, False],
                          [0o600, False, False, False],
                          [0o700, False, False, False],
                          [0o000, False, False, False],
                          [0o010, False, False, True],
                          [0o020, False, True, False],
                          [0o030, False, True, True],
                          [0o040, True, False, False],
                          [0o050, True, False, True],
                          [0o060, True, True, False],
                          [0o070, True, True, True],
                          [0o000, False, False, False],
                          [0o001, False, False, False],
                          [0o002, False, False, False],
                          [0o003, False, False, False],
                          [0o004, False, False, False],
                          [0o005, False, False, False],
                          [0o006, False, False, False],
                          [0o007, False, False, False],
                          [0o777, True, True, True]])
def test_get_group_permissions(chmod_mask, read, write, execute):
    with NamedTemporaryFile() as tmp_file:
        os.chmod(tmp_file.name, chmod_mask)
        path = Path(tmp_file.name)
        assert file_helpers.get_group_permissions(path) == (read, write, execute)


@pytest.mark.parametrize("chmod_mask,read,write,execute",
                         [[0o000, False, False, False],
                          [0o100, False, False, False],
                          [0o200, False, False, False],
                          [0o300, False, False, False],
                          [0o400, False, False, False],
                          [0o500, False, False, False],
                          [0o600, False, False, False],
                          [0o700, False, False, False],
                          [0o000, False, False, False],
                          [0o010, False, False, False],
                          [0o020, False, False, False],
                          [0o030, False, False, False],
                          [0o040, False, False, False],
                          [0o050, False, False, False],
                          [0o060, False, False, False],
                          [0o070, False, False, False],
                          [0o000, False, False, False],
                          [0o001, False, False, True],
                          [0o002, False, True, False],
                          [0o003, False, True, True],
                          [0o004, True, False, False],
                          [0o005, True, False, True],
                          [0o006, True, True, False],
                          [0o007, True, True, True],
                          [0o777, True, True, True]])
def test_get_world_permissions(chmod_mask, read, write, execute):
    with NamedTemporaryFile() as tmp_file:
        os.chmod(tmp_file.name, chmod_mask)
        path = Path(tmp_file.name)
        assert file_helpers.get_world_permissions(path) == (read, write, execute)


def test_assert_secure_dir_raises_exception_on_non_existant_path():
    """Ensure that `assert_secure_dir` raises an error if `path` does not exist"""
    directory = "/foo/bar/biz"
    bad_path = Path(directory)
    with pytest.raises(ValueError) as excinfo:
        file_helpers.assert_secure_dir(bad_path)
    assert excinfo.value.args[0] == f"{directory} does not exist"


def test_assert_secure_dir_raises_exception_on_file_path():
    """Ensure that `assert_secure_dir` raises an error if `path` is not a directory"""
    with NamedTemporaryFile() as tmp_file:
        with pytest.raises(ValueError) as excinfo:
            file_helpers.assert_secure_dir(Path(tmp_file.name))
        assert excinfo.value.args[0] == f"{tmp_file.name} is not a directory"


@pytest.mark.parametrize("permissions", [0o701, 0o702, 0o703, 0o704, 0o705, 0o706, 0o707,
                                         0o710, 0o720, 0o730, 0o740, 0o750, 0o760, 0o770])
def test_assert_secure_dir_rejects_dir_without_700_perms(permissions):
    """Ensure that `assert_secure_dir` requires the `path`
    to have 700 permissions.
    """
    with TemporaryDirectory() as tmp_dir:
        os.chmod(tmp_dir, permissions)
        with pytest.raises(PermissionException):
            file_helpers.assert_secure_dir(Path(tmp_dir))


def test_assert_secure_dir_accepts_dir_with_700_perms():
    """Ensure that `assert_secure_dir` accepts a directory
    with permissions set to 700.
    """
    with TemporaryDirectory() as tmp_dir:
        os.chmod(tmp_dir, 0o700)
        file_helpers.assert_secure_dir(Path(tmp_dir))
