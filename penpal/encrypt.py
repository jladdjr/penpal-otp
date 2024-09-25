from pathlib import Path

from penpal.archive import Archiver
from penpal.utils.file_helpers import assert_secure_dir, tmp_directory


class Encrypter:
    """Given a path to a one-time pad, encrypts a file or directory
    using the following steps:

    - Creates a tar-gzipped archive of the file or directory to encrypt
      - This reduces the size of the file to encrypt
      - Converts directories to a single file
      - Preserves file metadata
    - Uses blocks from a one-time pad to encrypt the archive file,
      deleting each block as it is used as a safeguard against
      reusing portions of the pad
    - Records which blocks were used for encryption
    - Records how many bytes of the final block were needed
    - Creates a final tar-gzipped archive of the block list and the
      encrypted file itself
    """

    @staticmethod
    def preflight_check(pad_path: Path, file_path: Path, encrypted_file_path: Path):
        """Ensures preconditions for encrypting are met.

        Arguments:
        pad_path -- path to one-time pad
        file_path -- file to encrypt
        encrypted_file_path -- location to store encrypted file
        """
        if not pad_path.exists():
            raise ValueError(f"Could not find one-time pad at {pad_path}")
        if not file_path.exists():
            raise ValueError(f"Could not find file at {file_path}")

        assert_secure_dir(pad_path)

        Archiver.preflight_check()

        # TODO: if pad directory is empty, raise an exception

    @staticmethod
    def encrypt(pad_path: Path, file_path: Path, encrypted_file_path: Path):
        """Encrypts a file using a one-time pad located at `pad`.

        Note that the `encrypted_file_path` must be located in a folder
        with file permissions set to 0o700.

        Arguments:
        pad_path -- path to one-time pad
        file_path -- file to encrypted
        encrypted_file_path -- location to store encrypted file
        """
        Encrypter.preflight_check(pad_path, file_path, encrypted_file_path)

        # TODO: create hook to clean up tmp directory
        #       call hook if there are any exceptions
        #       (wrap whole operation below in try / except Exception)
        tmp_dir = tmp_directory()
        archived_file_path = Path(tmp_dir.name).joinpath("content.tgz")

        Archiver.create_archive(source_file=file_path,
                                dest_file=archived_file_path)

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
