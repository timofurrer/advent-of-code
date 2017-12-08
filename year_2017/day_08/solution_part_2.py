"""
Solution for the first puzzle of Day 4
"""

import os
import operator
import functools
from collections import namedtuple, defaultdict
from typing import Tuple, List

import pytest

# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


Instruction = namedtuple('Instruction', [
    'target_operator',
    'cond_operator',
])


OPERATORS = {
    'inc': operator.add,
    'dec': operator.sub,
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le
}


def parse_input(raw_instructions: str) -> List[Instruction]:
    """
    Parse instructions
    """
    instructions = []
    for raw_instruction in raw_instructions.splitlines():
        (target_register, target_operator, target_value,
                _, cond_register, cond_operator, cond_value) = raw_instruction.split()

        def __target_operator(target_register, target_operator, target_value, registers):
            registers[target_register] = OPERATORS[target_operator](
                    registers[target_register], int(target_value))

        def __cond_operator(cond_register, cond_operator, cond_value, registers):
            return OPERATORS[cond_operator](
                    registers[cond_register], int(cond_value))

        target_operator_func = functools.partial(
                __target_operator, target_register,
                target_operator, target_value)
        cond_operator_func = functools.partial(
                __cond_operator, cond_register, cond_operator, cond_value)

        instructions.append(
                Instruction(target_operator_func, cond_operator_func))

    return instructions


def run_instructions(instructions: List[Instruction]) -> Tuple[dict, int]:
    """
    Run instructions and return registers
    """
    registers = defaultdict(lambda: 0)
    max_value = 0
    for instruction in instructions:
        if instruction.cond_operator(registers):
            instruction.target_operator(registers)

        current_max_value = max(registers.values())
        if current_max_value > max_value:
            max_value = current_max_value

    return registers, max_value


def find_largest_register_value(instructions: list) -> int:
    """
    Find the largest register value
    """
    registers, max_value = run_instructions(instructions)
    return max_value


@pytest.mark.parametrize('raw_instructions, expected_value', [
    (open(os.path.join(os.path.dirname(__file__),
                       'sample_input.txt')).read(), 10),
    # my puzzle input
    (open(MY_PUZZLE_INPUT).read(), 5443)
])
def test_find_largest_register_value(raw_instructions, expected_value):
    """Test the solution"""
    # given
    parsed_input = parse_input(raw_instructions)

    # when
    actual_value = find_largest_register_value(parsed_input)

    # then
    assert actual_value == expected_value
