import os
from pathlib import Path

import yaml

from penpal.archive import Archiver
from penpal.hazmat.hazmat import xor_encrypt
from penpal.pad import fetch_and_destroy_random_block
from penpal.utils.file_helpers import (assert_secure_dir,
                                       tmp_directory)



class Encrypter:
    """Given a path to a one-time pad, encrypts a file using the
    following steps:

    - Creates a tar-gzipped archive of the file or directory to encrypt
      - This reduces the size of the file to encrypt
      - Converts directories to a single file
      - Preserves file metadata
    - Uses blocks from a one-time pad to encrypt the archive file,
      deleting each block as it is used as a safeguard against
      reusing portions of the pad
    - Records which blocks were used for encryption
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

        Archiver.create_archive(source_files=[file_path],
                                dest_file=archived_file_path)

        enc_file_bytes = bytearray()
        block_names = []

        with open(archived_file_path, 'rb') as archived_file:
            finished = False
            while not finished:
                # TODO: Catch EmptyOneTimePadException
                name, key = fetch_and_destroy_random_block(pad_path)
                block_names.append(name)

                cleartext = archived_file.read(len(key))

                if len(cleartext) < len(key):
                    # this is the last block to encode
                    finished = True
                    key = key[:len(cleartext)]

                enc_file_bytes.extend(xor_encrypt(cleartext, key))

        # TODO: call clean-up hooks

        # write manifest file
        manifest_path = Path(tmp_dir.name).joinpath("manifest")
        with open(manifest_path, "w") as manifest:
            yaml.dump(block_names, manifest, default_flow_style=False)

        ciphertext_path = Path(tmp_dir.name).joinpath("cipher.bin")
        with open(ciphertext_path, "wb") as cipher_file:
            cipher_file.write(enc_file_bytes)

        # Use tar to create a compressed archive from message.enc
        Archiver.create_archive(source_files=[manifest_path, ciphertext_path],
                                dest_file=encrypted_file_path)

        # Delete temporary directory
        tmp_dir.cleanup()
