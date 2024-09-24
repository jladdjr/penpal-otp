from pathlib import Path

from penpal.utils.file_helpers import assert_secure_dir


def encrypt(pad_path: Path, file_path: Path, encrypted_file_path: Path):
    """Encrypts a file using a one-time pad located at `pad`.

    Note that the `encrypted_file_path` must be located in a folder
    with file permissions set to 0o700.

    Arguments:
    pad_path -- path to one-time pad
    file_path -- file to encrypted
    encrypted_file_path -- location to store encrypted file
    """
    if not pad_path.exists():
        raise ValueError(f"Could not find one-time pad at {pad_path}")
    if not file_path.exists():
        raise ValueError(f"Could not find file at {file_path}")

    assert_secure_dir(pad_path)

    # TODO: if pad directory is empty, raise an exception

    # TODO: create clean-up hooks that can be called if encryption finishes
    #       successfully, or if it is interrupted

    # pseudocode
    # create temporary working directory
    #   and assign 0o700-level permissions to dir
    #   and make sure that folder is under user's directory
    #
    # use tar to create a compressed archive of the original file
    #   .. so that the file's metadata can be preserved
    #
    # create variable to hold encrypted bytes
    # create list to hold filenames of all blocks used
    #   and a count of the number of bytes used for
    #   encryption in the final block
    #
    # open tar archive to encrypt (w/ 'rb' mode)
    # create variable to use to note when encryption has completed
    #
    # while True
    #  TODO: consider making the contents of this loop a helper function
    #
    #  fetch a block from otp
    #    if there are no more blocks left, raise an exception
    #    read the block into memory
    #    then delete the file from the otp
    #
    #  get length of block
    #  determine how many bytes to encrypt on this pass
    #    should be the length of the block
    #    or the length of the remainder of the file
    #    whichever is smaller
    #    if this is the final pass note so
    #      and save number of bytes encrypted using final block
    #      in the array
    #
    #  encrypt that many bytes of the file
    #  .. and save the result in the array of bytes for the encrypted file
    #
    #  if this is the final pass, break from the loop
    #
    # (outside of encryption loop)
    # call clean-up hooks
    # create temporary directory to hold encrypted message and manifest
    #  .. call directory message.enc
    # write manifest to directory
    # write encrypted binary file to directory
    #
    # Use tar to create a compressed archive from message.enc
    # Delete message.enc
    # Give the encrypted message the name requested by the user
