"""
Solution for the first puzzle of Day 23
"""

import os
from collections import defaultdict

import pytest

# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


def is_number(x):
    try:
        int(x)
    except ValueError:
        return False
    else:
        return True


def parse_instructions(raw_instructions):
    instructions = []
    for raw_instruction in raw_instructions.splitlines():
        instructions.append(raw_instruction.split())
    return instructions


def evaluate_register_h(instructions):
    b = c = d = e = f = h = 0

    b = 108100
    c = 125100

    while True:
        # f = 1
        f = True
        d = 2
        while True:
            e = 2
            while True:
                if d * e == b:
                    f = False
                e = e + 1
                if e == b:
                    break

            d = d + 1
            if d == b:
                break

        if f is False:
            h = h + 1

        if b == c:
            break

        b = b + 17
    return h


@pytest.mark.parametrize('input_file, expected_register_h_value', [
    # my puzzle input
    (MY_PUZZLE_INPUT, 0)
])
def test_evaluate_register_h(input_file, expected_register_h_value):
    """Test the solution"""
    # given
    with open(input_file) as f:
        instructions = parse_instructions(f.read())

    # when
    actual_register_h_value = evaluate_register_h(instructions)

    # then
    assert actual_register_h_value == expected_register_h_value
