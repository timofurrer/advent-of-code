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


def a_billion_dances(programs, instructions):
    """
    Make them dance a billion times!
    """
    generated_programs = []
    for i in range(1_000_000_000):
        p = ''.join(programs)
        if p in generated_programs:
            return list(generated_programs[1_000_000_000 % i])

        generated_programs.append(p)

        programs = dance(programs, instructions)

    return programs


@pytest.mark.parametrize('raw_dance_instructions, given_programs_order, expected_programs_order', [
    # my puzzle input
    (open(MY_PUZZLE_INPUT).read().strip(), list('abcdefghijklmnop'), list('lgmkacfjbopednhi'))
])
def test_a_billion_dances(
        raw_dance_instructions, given_programs_order, expected_programs_order):
    """Test the solution"""
    # given
    dance_instructions = raw_dance_instructions.split(',')

    # when
    actual_programs_order = a_billion_dances(
            given_programs_order, dance_instructions)

    # then
    assert actual_programs_order == expected_programs_order
