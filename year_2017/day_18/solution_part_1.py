"""
Solution for the first puzzle of Day 18
"""

import os
from collections import defaultdict

import pytest


SAMPLE_INPUT = os.path.join(os.path.dirname(__file__), 'sample_input.txt')
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


def recover_first_frequency(instructions):
    last_played_sound = None
    registers = defaultdict(int)

    def reg_value(x):
        return int(x) if is_number(x) else registers[x]

    i = 0
    while i < len(instructions):
        instruction, *arguments = instructions[i]
        if instruction == 'snd':
            last_played_sound = registers[arguments[0]]
        elif instruction == 'set':
            X, Y = arguments
            registers[X] = reg_value(Y)
        elif instruction == 'add':
            X, Y = arguments
            registers[X] += reg_value(Y)
        elif instruction == 'mul':
            X, Y = arguments
            registers[X] *= reg_value(Y)
        elif instruction == 'mod':
            X, Y = arguments
            registers[X] %= reg_value(Y)
        elif instruction == 'rcv':
            if registers[arguments[0]] != 0:
                return last_played_sound
        elif instruction == 'jgz':
            X, Y = arguments
            if reg_value(X) > 0:
                i += reg_value(Y)
                continue
        else:
            raise ValueError(f'unknown instruction {instruction}')

        i += 1

    return None


@pytest.mark.parametrize('input_file, expected_first_recovered_freq', [
    (SAMPLE_INPUT, 4),
    # my puzzle input
    (MY_PUZZLE_INPUT, 7071)
])
def test_recover_first_frequency(input_file, expected_first_recovered_freq):
    """Test the solution"""
    # given
    with open(input_file) as f:
        instructions = parse_instructions(f.read())

    # when
    actual_first_recovered_freq = recover_first_frequency(instructions)

    # then
    assert actual_first_recovered_freq == expected_first_recovered_freq
