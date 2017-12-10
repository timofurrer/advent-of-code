"""
Solution for the first puzzle of Day 4
"""

import os

import pytest

# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


def calc_group_score(stream: str) -> int:
    """
    Calculate the group score
    """
    level = 0
    score = 0
    in_garbage = False
    i = 0
    while i < len(stream):
        char = stream[i]

        if in_garbage:
            if char == '!':
                i += 1
            elif char == '>':
                in_garbage = False
        else:
            if char == '{':
                level += 1
            elif char == '}':
                score += level
                level -= 1
            elif char == '<':
                in_garbage = True

        i += 1

    return score


@pytest.mark.parametrize('stream, expected_score', [
    ('{}', 1),
    ('{{{}}}', 6),
    ('{{},{}}', 5),
    ('{{{},{},{{}}}}', 16),
    ('{<a>,<a>,<a>,<a>}', 1),
    ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
    ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
    ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3),
    # my puzzle input
    (open(MY_PUZZLE_INPUT).read(), 9251)
])
def test_calc_group_score(stream, expected_score):
    """Test the solution"""
    # given & when
    actual_score = calc_group_score(stream)

    # then
    assert actual_score == expected_score
