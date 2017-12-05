"""
Solution for the first puzzle of Day 4
"""

import os
from typing import List

import pytest

# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_input(instructions: str) -> List[int]:
    """
    Maze instructions
    """
    return [int(l) for l in instructions.splitlines()]


def escape_maze(instructions: List[int]) -> int:
    """
    Return the amount of steps to take before the maze is exited
    """
    current_index = 0
    steps = 0
    while current_index < len(instructions):
        jumps = instructions[current_index]
        if jumps >= 3:
            instructions[current_index] -= 1
        else:
            instructions[current_index] += 1
        current_index += jumps
        steps += 1

    return steps


@pytest.mark.parametrize('instructions, expected_steps', [
    ('0\n3\n0\n1\n-3\n', 10),
    # my puzzle input
    (open(MY_PUZZLE_INPUT).read(), 26889114)
])
def test_escape_maze(instructions, expected_steps):
    """Test the solution"""
    # given
    parsed_input = parse_input(instructions)

    # when
    actual_steps = escape_maze(parsed_input)

    # then
    assert actual_steps == expected_steps
