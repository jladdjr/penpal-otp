import os
from pathlib import Path

import yaml

from penpal.archive import Archiver
from penpal.hazmat.hazmat import xor_encrypt
from penpal.pad import fetch_and_destroy_random_block
from penpal.utils.file_helpers import (assert_secure_dir,
                                       tmp_directory)



class Decrypter:
    """Given a path to a one-time pad, decrypts a file using the
    following steps:

    - The encrypted file is actually a tar-gzipped archive.
      The first step, then, is to unarchive this file.
      This results in a block list and the encrypted file itself
    - The blocks in the block list are retrieved one at a time
      and used to decrypt the encrypted file
    - Each block that is retrieved is also deleted as a safeguard against
      reusing portions of the pad
    - The original encrypted file is deleted
    - The decrypted file is created in the same directory where the
      encrypted file was located
    """

    @staticmethod
    def preflight_check(pad_path: Path, encrypted_file_path: Path):
        """Ensures preconditions for decryption are met.

        Arguments:
        pad_path -- path of one-time pad
        encrypted_file_path -- path of encrypted file
        """
        if not pad_path.exists():
            raise ValueError(f"Could not find one-time pad at {pad_path}")
        if not encrypted_file_path.exists():
            raise ValueError(f"Could not find encrypted file at {encrypted_file_path}")

        assert_secure_dir(pad_path)

        Archiver.preflight_check()

        # TODO: if pad directory is empty, raise an exception

    @staticmethod
    def decrypt(pad_path: Path, encrypted_file_path: Path):
        """Decrypts a file using a one-time pad located at `pad`.

        Note that the `encrypted_file_path` must be located in a folder
        with file permissions set to 0o700.

        Arguments:
        pad_path -- path of one-time pad
        encrypted_file_path -- path of encrypted file
        """
        Denrypter.preflight_check(pad_path, encrypted_file_path)

        Archiver.extract_archive(encrypted_file_path)
        decrypted_file_bytes = bytearray()
        encrypted_message_path = encrypted_message_path.parent().joinpath("cipher.bin")

        with open(encrypted_message_path, 'rb') as ciphertext:
            finished = False
            while not finished:
                # TODO: Catch EmptyOneTimePadException
                # TODO: bookmark
                name, key = fetch_and_destroy_random_block(pad_path)
                block_names.append(name)

                cleartext = archived_file.read(len(key))

                if len(cleartext) < len(key):
                    # this is the last block to encode
                    finished = True
                    final_bytes_used = len(cleartext)
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
