############################################################
# hazmat.py                                                #
#                                                          #
# !!! WARNING !!!                                          #
# CONTAINS FUNCTIONS THAT ARE CRYPTOGRAPHICALLY SENSITIVE. #
############################################################

from os import urandom


def get_random_bytes(length: int) -> bytes:
    """TODO: explain why os.urandom instead of random is used here
    """
    return urandom(length)
