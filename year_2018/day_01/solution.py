"""
Solution for the first puzzle of Day 1
"""

import os
import itertools

from typing import List

import pytest

# My puzzle input
with open(os.path.join(os.path.dirname(__file__), "input.txt")) as input_file:
    MY_PUZZLE_INPUT = [int(x) for x in input_file.readlines()]


def part_1_calibrate_device(frequency_changes: List[int]) -> int:
    """
    """
    frequency = sum(frequency_changes)
    return frequency


def part_2_duplicate_frequency(frequency_changes: List[int]):
    """
    """
    previous_frequencies = set()
    current_frequency = 0
    for frequency_change in itertools.cycle(frequency_changes):
        previous_frequencies.add(current_frequency)
        current_frequency += frequency_change
        if current_frequency in previous_frequencies:
            return current_frequency
    return None


@pytest.mark.parametrize('frequency_changes, expected_frequency', [
    ([+1, +1, +1], 3),
    ([+1, +1, -2], 0),
    ([-1, -2, -3], -6),
    # my puzzle input
    (MY_PUZZLE_INPUT, 531)
])
def test_solution_part_1(frequency_changes, expected_frequency):
    """Test the solution"""
    # given & when
    actual_frequency = part_1_calibrate_device(frequency_changes)

    # then
    assert actual_frequency == expected_frequency


@pytest.mark.parametrize('frequency_changes, expected_first_duplicate_freq', [
    ([+1, -1], 0),
    ([+3, +3, +4, -2, -4], 10),
    ([-6, +3, +8, +5, -6], 5),
    ([+7, +7, -2, -7, -4], 14),
    # my puzzle input
    (MY_PUZZLE_INPUT, 76787)
])
def test_solution_part_2(frequency_changes, expected_first_duplicate_freq):
    """Test the solution"""
    # given & when
    actual_first_duplicate_freq = part_2_duplicate_frequency(frequency_changes)

    # then
    assert actual_first_duplicate_freq == expected_first_duplicate_freq
