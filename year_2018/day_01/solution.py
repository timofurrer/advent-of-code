"""
Solution for the first puzzle of Day 1
"""

from typing import List

import pytest

# My puzzle input
with open("input.txt") as input_file:
    MY_PUZZLE_INPUT = [int(x) for x in input_file.readlines()]


def calibrate_device(frequency_changes: List[int]) -> int:
    """
    Calibrate the device
    """
    frequency = sum(frequency_changes)
    return frequency


@pytest.mark.parametrize('frequency_changes, expected_frequency', [
    ([+1, +1, +1], 3),
    ([+1, +1, -2], 0),
    ([-1, -2, -3], -6),
    # my puzzle input
    (MY_PUZZLE_INPUT, 531)
])
def test_solution(frequency_changes, expected_frequency):
    """Test the solution"""
    # given & when
    actual_frequency = calibrate_device(frequency_changes)

    # then
    assert actual_frequency == expected_frequency
