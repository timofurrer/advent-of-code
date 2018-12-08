"""
Solution for the first puzzle of Day 1
"""

import os

from typing import List, Optional

import pytest

import numpy as np

# My puzzle input
with open(os.path.join(os.path.dirname(__file__), "input.txt")) as input_file:
    MY_PUZZLE_INPUT = [x.strip() for x in input_file.readlines()]


def parse_claim(raw_claim):
    claim_id, rest = raw_claim.split("@")
    coords, size = rest.split(":")
    x, y = coords.split(",")
    width, height = size.split("x")
    return (
        int(claim_id[1:].strip()),
        int(x.strip()), int(y.strip()),
        int(width.strip()), int(height.strip())
    )


def part_1_calculate_overlaps(raw_claims: List[str]) -> int:
    """
    """
    fabric_square = np.zeros((1000, 1000))
    for _, x, y, w, h in (parse_claim(c) for c in raw_claims):
        # add 1 to every inch of the claim
        fabric_square[x:x + w, y:y + h] += 1

    # where ever there were two or more claims on the fabric inch
    return np.size(np.where(fabric_square >= 2)[0])


def part_2_get_non_overlapping_claim(raw_claims: List[str]) -> int:
    """
    """
    fabric_square = np.zeros((1000, 1000))
    claim_areas = []
    for claim_id, x, y, w, h in (parse_claim(c) for c in raw_claims):
        # add 1 to every inch of the claim
        fabric_square[x:x + w, y:y + h] += 1
        claim_areas.append((claim_id, x, y, w, h))

    # find the claim which does not overlap
    for claim_id, x, y, w, h in claim_areas:
        if (fabric_square[x:x + w, y:y + h] == 1).all():
            return claim_id


@pytest.mark.parametrize("claims, expected_overlap", [
    # my puzzle input
    (MY_PUZZLE_INPUT, 118322)
])
def test_solution_part_1(claims, expected_overlap):
    """Test the solution"""
    # given & when
    actual_overlap = part_1_calculate_overlaps(claims)

    # then
    assert actual_overlap == expected_overlap


@pytest.mark.parametrize("claims, expected_non_overlapping_claim", [
    # my puzzle input
    (MY_PUZZLE_INPUT, 118322)
])
def test_solution_part_3(claims, expected_non_overlapping_claim):
    """Test the solution"""
    # given & when
    actual_non_overlapping_claim = part_2_get_non_overlapping_claim(claims)

    # then
    assert actual_non_overlapping_claim == expected_non_overlapping_claim
