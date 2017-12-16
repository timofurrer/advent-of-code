"""
Solution for the first puzzle of Day 14
"""

import pytest

from year_2017.day_10.solution_part_2 import knothash


# My puzzle input
MY_PUZZLE_INPUT = 'ugkiagan'


def calc_used_squares(input_hash):
    """
    Calculate the used squares by the given hash
    """
    used = 0
    for i in range(128):
        knot_hash = knothash(input_hash + '-' + str(i))
        binhash = bin(int(knot_hash, 16))
        used += sum(int(x) for x in binhash[2:])

    return used


@pytest.mark.parametrize('input_hash, expected_used_squares', [
    ('flqrgnkx', 8108),
    # my puzzle input
    (MY_PUZZLE_INPUT, 8292)
])
def test_calc_used_squares(input_hash, expected_used_squares):
    """Test the solution"""
    # given & when
    actual_used_squares = calc_used_squares(input_hash)

    # then
    assert actual_used_squares == expected_used_squares
