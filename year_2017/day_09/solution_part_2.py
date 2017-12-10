"""
Solution for the first puzzle of Day 4
"""

import os

import pytest

# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


def count_garbage(stream: str) -> int:
    """
    Count the garbage in the stream
    """
    level = 0
    garbage = 0
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
                garbage += 1
        else:
            if char == '{':
                level += 1
            elif char == '}':
                level -= 1
            elif char == '<':
                in_garbage = True

        i += 1

    return garbage


@pytest.mark.parametrize('stream, expected_garbage', [
    ('<>', 0),
    ('<random characters>', 17),
    ('<<<<>', 3),
    ('<{!>}>', 2),
    ('<!!>', 0),
    ('<!!!>>', 0),
    ('<{o"i!a,<{i<a>', 10),
    # my puzzle input
    (open(MY_PUZZLE_INPUT).read(), 4322)
])
def test_count_garbage(stream, expected_garbage):
    """Test the solution"""
    # given & when
    actual_garbage = count_garbage(stream)

    # then
    assert actual_garbage == expected_garbage
