"""
Solution for the first puzzle of Day 15
"""

import pytest


GENERATOR_A_FACTOR = 16807
GENERATOR_B_FACTOR = 48271
DIVIDER = 2147483647

# My puzzle input
MY_PUZZLE_INPUT = 591, 393


def generate_next_pair(value, factor):
    while True:
        value *= factor
        value %= DIVIDER

        yield value


def count_matches(gen_a_start, gen_b_start, pairs):
    """
    Count matches of Generator A and B
    """
    matches = 0
    gen_a = generate_next_pair(gen_a_start, GENERATOR_A_FACTOR)
    gen_b = generate_next_pair(gen_b_start, GENERATOR_B_FACTOR)

    for _ in range(pairs):
        a, b = next(gen_a), next(gen_b)

        # compare bits
        if a & 0xFFFF == b & 0xFFFF:
            matches += 1

    return matches


@pytest.mark.parametrize('gen_a_start, gen_b_start, pairs, expected_matches', [
    (65, 8921, 40_000_000, 588),
    # my puzzle input
    (*MY_PUZZLE_INPUT, 40_000_000, 619)
])
def test_count_matches(gen_a_start, gen_b_start, pairs, expected_matches):
    """Test the solution"""
    # given & when
    actual_matches = count_matches(gen_a_start, gen_b_start, pairs)

    # then
    assert actual_matches == expected_matches
