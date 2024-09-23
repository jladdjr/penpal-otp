############################################################
# hazmat.py                                                #
#                                                          #
# !!! WARNING !!!                                          #
# CONTAINS FUNCTIONS THAT ARE CRYPTOGRAPHICALLY SENSITIVE. #
############################################################

from os import urandom


def get_random_bytes(length: int) -> bytes:
    """os.urandom retrieves random bytes produced by the operating system
    (for example, /dev/urandom) that are sufficient for cryptographic applications.

    This function avoids calling random.randbytes which is intended for simulations
    and is *not* suitable for security applications.
    """
    return urandom(length)
