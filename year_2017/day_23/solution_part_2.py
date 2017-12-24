"""
Solution for the first puzzle of Day 23
"""

import pytest


def count_primes():
    # input values
    b = 108100
    c = 125100

    h = 0
    while True:
        f = True
        for d in range(2, b):
            if b % d == 0:
                f = False
                break

        if f is False:
            h = h + 1

        if b == c:
            break

        b = b + 17
    return h


@pytest.mark.parametrize('expected_register_h_value', [
    909
])
def test_count_primes(expected_register_h_value):
    """Test the solution"""
    # given
    # when
    actual_register_h_value = count_primes()

    # then
    assert actual_register_h_value == expected_register_h_value
