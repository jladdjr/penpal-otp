from pathlib import Path
from tempfile import TemporaryDirectory


def get_or_create_pad_directory():
    """Gets directory used to store one-time pads
    and create temporary directories for encrypting and decrypting files.

    By default, this is `$HOME/.pad`
    """
    # TODO: make pad directory configurable
    pad_dir = Path("~/.pad").expanduser()

    if not pad_dir.exists():
        pad_dir.mkdir(0o700)
    return pad_dir


def tmp_directory():
    """Gets temporary directory suitable for encrypting
    or decrypting files.

    This will be created under the pad directory.
    """
    pad_dir = get_or_create_pad_directory()

    return TemporaryDirectory(dir=pad_dir)
