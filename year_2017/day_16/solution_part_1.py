"""
Solution for the first puzzle of Day 16
"""

import os

import pytest


# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


def exchange(p, a, b):
    p[a], p[b] = p[b], p[a]
    return p


def partner(p, a, b):
    a_i, b_i = p.index(a), p.index(b)
    return exchange(p, a_i, b_i)


DANCE_MOVES = {
    's': lambda p, n: p[-int(n):] + p[:-int(n)],
    'x': lambda p, a, b: exchange(p, int(a), int(b)),
    'p': partner
}


def dance(programs, instructions):
    """
    Make the programs dance!
    """
    for instruction in instructions:
        move_func = DANCE_MOVES[instruction[0]]
        programs = move_func(programs, *instruction[1:].split('/'))

    return programs


@pytest.mark.parametrize('raw_dance_instructions, given_programs_order, expected_programs_order', [
    ('s1,x3/4,pe/b', list('abcde'), list('baedc')),
    # my puzzle input
    (open(MY_PUZZLE_INPUT).read().strip(), list('abcdefghijklmnop'), list('fgmobeaijhdpkcln'))
])
def test_dance(
        raw_dance_instructions, given_programs_order, expected_programs_order):
    """Test the solution"""
    # given
    dance_instructions = raw_dance_instructions.split(',')

    # when
    actual_programs_order = dance(given_programs_order, dance_instructions)

    # then
    assert actual_programs_order == expected_programs_order
