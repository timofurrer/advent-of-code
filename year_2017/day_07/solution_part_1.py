"""
Solution for the first puzzle of Day 4
"""

import os
import re
from collections import namedtuple

import pytest

# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


Program = namedtuple('Program', ['name', 'weight'])


def parse_input(raw_programs: str) -> dict:
    """
    Parse tower input
    """
    programs = {}
    for raw_program in raw_programs.splitlines():
        name = raw_program.split()[0]
        weight = re.search(r'\((\d+)\)', raw_program).group(1)
        program = Program(name, weight)
        if '->' in raw_program:
            sub_programs = raw_program.split('->', maxsplit=1)[-1]
            programs[program] = [
                    Program(x, 0) for x in sub_programs.strip().split(', ')]
        else:
            programs[program] = []

    return programs


def find_root_program(programs: dict) -> int:
    """
    Find the root program
    """
    # holds all nodes which are not a leaf
    nodes = {k: v for k, v in programs.items() if len(v) > 0}
    for program, sub_programs in nodes.items():
        if program.name not in (p.name for sp in nodes.values() for p in sp):
            return program.name

    return None


@pytest.mark.parametrize('programs, expected_root', [
    (open(os.path.join(os.path.dirname(__file__),
                       'sample_input.txt')).read(), 'tknk'),
    # my puzzle input
    (open(MY_PUZZLE_INPUT).read(), 'ahnofa')
])
def test_find_root_program(programs, expected_root):
    """Test the solution"""
    # given
    parsed_input = parse_input(programs)

    # when
    actual_root = find_root_program(parsed_input)

    # then
    assert actual_root == expected_root
