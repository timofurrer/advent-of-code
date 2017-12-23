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


def count_mul_invokes(instructions):
    mul_invokes = 0
    registers = defaultdict(int)

    def reg_value(x):
        return int(x) if is_number(x) else registers[x]

    i = 0
    while i < len(instructions):
        instruction, *arguments = instructions[i]
        if instruction == 'set':
            X, Y = arguments
            registers[X] = reg_value(Y)
        elif instruction == 'sub':
            X, Y = arguments
            registers[X] -= reg_value(Y)
        elif instruction == 'mul':
            mul_invokes += 1
            X, Y = arguments
            registers[X] *= reg_value(Y)
        elif instruction == 'jnz':
            X, Y = arguments
            if reg_value(X) != 0:
                i += reg_value(Y)
                continue
        else:
            raise ValueError(f'unknown instruction {instruction}')

        i += 1

    return mul_invokes


@pytest.mark.parametrize('input_file, expected_mul_invokes', [
    # my puzzle input
    (MY_PUZZLE_INPUT, 6241)
])
def test_count_mul_invokes(input_file, expected_mul_invokes):
    """Test the solution"""
    # given
    with open(input_file) as f:
        instructions = parse_instructions(f.read())

    # when
    actual_mul_invokes = count_mul_invokes(instructions)

    # then
    assert actual_mul_invokes == expected_mul_invokes
