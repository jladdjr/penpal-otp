from unittest import mock

from penpal.hazmat import hazmat


@mock.patch("penpal.hazmat.hazmat.urandom")
def test_get_random_bytes(urandom):
    byte_array = [1, 2, 3, 4, 5]
    urandom.return_value = bytes(byte_array)
    result = hazmat.get_random_bytes(10)
    assert result == bytes(byte_array)
