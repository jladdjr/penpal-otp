from pathlib import Path

from noirnet.archive import Archiver
from noirnet.utils.file_helpers import tmp_directory


class Encrypter:
    """Given a path to a one-time pad, encrypts a file or directory
    using the following steps:

    - Uses blocks from a one-time pad to encrypt the target file,
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

        Archiver.preflight_check()

        # TODO: if pad directory is empty, raise an exception

    @staticmethod
    def encrypt(pad_path: Path, file_path: Path, encrypted_file_path: Path):
        """Encrypts a file using a one-time pad located at `pad`.

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

        enc_file_bytes = bytearray()
        block_names = []

        with open(file_path, "rb") as file:
            finished = False
            while not finished:
                # TODO: Catch EmptyOneTimePadException
                name, key = fetch_and_destroy_random_block(pad_path)
                block_names.append(name)

                cleartext = file.read(len(key))

                if len(cleartext) < len(key):
                    # this is the last block to encode
                    finished = True
                    key = key[: len(cleartext)]

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
        Archiver.create_archive(
            source_files=[manifest_path, ciphertext_path], dest_file=encrypted_file_path
        )

        # Delete temporary directory
        tmp_dir.cleanup()
