"""
Solution for the first puzzle of Day 18
"""

import os
import string

import pytest


SAMPLE_INPUT = os.path.join(os.path.dirname(__file__), 'sample_input.txt')
# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_diagram(raw_diagram):
    diagram = []
    for row in raw_diagram.splitlines():
        diagram.append(list(row))
    return diagram


NEIGHBORS = (
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
)


def letters_in_path(diagram):
    # find start
    # current_pos in Y, X
    current_pos = 0, diagram[0].index('|')

    # travel direction in Y, X
    direction = 1, 0

    # collected letters in path
    letters = ''

    # follow path until the end
    while diagram[current_pos[0]][current_pos[1]] != ' ':
        prev_pos = current_pos
        y, x = current_pos
        current_sign = diagram[y][x]
        if current_sign == '+':
            # change direction
            prev_pos = direction[0] * -1, direction[1] * -1
            for dy, dx in (n for n in NEIGHBORS if n != prev_pos):
                neighbor_y, neighbor_x = y + dy, x + dx
                if 0 <= neighbor_y and neighbor_y < len(diagram) \
                        and 0 <= neighbor_x \
                        and neighbor_x < len(diagram[neighbor_y]):

                    if diagram[neighbor_y][neighbor_x] != ' ':
                        current_pos = neighbor_y, neighbor_x
                        direction = dy, dx
                        break
        else:
            if current_sign in string.ascii_uppercase:
                letters += current_sign
            current_pos = y + direction[0], x + direction[1]

    return letters


@pytest.mark.parametrize('input_file, expected_letters', [
    (SAMPLE_INPUT, 'ABCDEF'),
    # my puzzle input
    (MY_PUZZLE_INPUT, 'MOABEUCWQS')
])
def test_letters_in_path(input_file, expected_letters):
    """Test the solution"""
    # given
    with open(input_file) as f:
        diagram = parse_diagram(f.read())

    # when
    actual_letters = letters_in_path(diagram)

    # then
    assert actual_letters == expected_letters
