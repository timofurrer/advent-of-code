"""
Solution for the first puzzle of Day 1
"""

import os
import collections

from typing import List, Optional

import pytest

# My puzzle input
with open(os.path.join(os.path.dirname(__file__), "input.txt")) as input_file:
    MY_PUZZLE_INPUT = [x.strip() for x in input_file.readlines()]


def part_1_calculate_checksum(box_ids: List[str]) -> int:
    """
    """
    twos = 0
    threes = 0
    for box_id in box_ids:
        counts = collections.Counter(box_id).values()
        if 2 in counts:
            twos += 1
        if 3 in counts:
            threes += 1
    return twos * threes


def part_2_find_correct_box_id_letters(box_ids: List[str]) -> Optional[str]:
    """
    """
    for current_box_id in box_ids:
        for other_box_id in (x for x in box_ids if x != current_box_id):
            matching_characters = [
                    a for a, b
                    in zip(current_box_id, other_box_id)
                    if a == b
            ]
            if len(matching_characters) == len(current_box_id) - 1:
                return "".join(matching_characters)
    return None


@pytest.mark.parametrize("box_ids, expected_checksum", [
    # my puzzle input
    (MY_PUZZLE_INPUT, 4980)
])
def test_solution_part_1(box_ids, expected_checksum):
    """Test the solution"""
    # given & when
    actual_checksum = part_1_calculate_checksum(box_ids)

    # then
    assert actual_checksum == expected_checksum


@pytest.mark.parametrize("box_ids, expected_common_letters", [
    # my puzzle input
    (MY_PUZZLE_INPUT, "qysdtrkloagnfozuwujmhrbvx")
])
def test_solution_part_2(box_ids, expected_common_letters):
    """Test the solution"""
    # given & when
    actual_common_letters = part_2_find_correct_box_id_letters(box_ids)

    # then
    assert actual_common_letters == expected_common_letters
