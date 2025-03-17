############################################################
# hazmat.py                                                #
#                                                          #
# !!! WARNING !!!                                          #
# CONTAINS FUNCTIONS THAT ARE CRYPTOGRAPHICALLY SENSITIVE. #
############################################################

from operator import xor
from os import urandom


def get_random_bytes(length: int) -> bytes:
    """os.urandom retrieves random bytes produced by the operating system
    (for example, /dev/urandom) that are sufficient for cryptographic applications.

    This function avoids calling random.randbytes which is intended for simulations
    and is *not* suitable for security applications.
    """
    return urandom(length)


def xor_encrypt(cleartext: bytes, key: bytes):
    assert len(cleartext) == len(key)
    return bytes(xor(i, j) for (i, j) in zip(cleartext, key))


xor_decrypt = xor_encrypt
