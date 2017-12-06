"""
Solution for the first puzzle of Day 4
"""

import copy
import operator
from typing import List

import pytest

# My puzzle input
MY_PUZZLE_INPUT = '0 5 10 0 11 14 13 4 11 8 8 7 1 4 12 11'


def parse_input(memory_banks: str) -> List[int]:
    """
    Memory banks
    """
    return [int(l) for l in memory_banks.split()]


def count_redistributions(memory_banks: List[int]) -> int:
    """
    Count the amount of redistributions until an infinite loop happens.

    It's a brute-force approach which simulates all redistributions
    """
    redistributions = []
    while memory_banks not in redistributions:
        redistributions.append(copy.copy(memory_banks))
        # find max bank
        max_bank_idx, max_bank_val = max(
                enumerate(memory_banks), key=operator.itemgetter(1))

        # take all from max bank
        memory_banks[max_bank_idx] = 0

        cycle_idx = max_bank_idx + 1
        while max_bank_val > 0:
            memory_banks[cycle_idx % len(memory_banks)] += 1
            cycle_idx += 1
            max_bank_val -= 1

    return len(redistributions)


@pytest.mark.parametrize('memory_banks, expected_redistributions', [
    ('0 2 7 0', 5),
    # my puzzle input
    (MY_PUZZLE_INPUT, 7864)
])
def test_count_redistribution(memory_banks, expected_redistributions):
    """Test the solution"""
    # given
    parsed_input = parse_input(memory_banks)

    # when
    actual_redistributions = count_redistributions(parsed_input)

    # then
    assert actual_redistributions == expected_redistributions
