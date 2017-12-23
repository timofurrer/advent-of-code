"""
Solution for the first puzzle of Day 22
"""

import os

import pytest


SAMPLE_INPUT = os.path.join(os.path.dirname(__file__), 'sample_input.txt')
# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_map(raw_map):
    grid = []
    for raw_row in raw_map.splitlines():
        grid.append([x == '#' for x in raw_row])
    return grid


ABS_DIRECTIONS = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}

REL_DIRECTIONS = {
    (0, -1): {'left': 'left', 'right': 'right'},
    (0, 1): {'left': 'right', 'right': 'left'},
    (-1, 0): {'left': 'down', 'right': 'up'},
    (1, 0): {'left': 'up', 'right': 'down'}
}


def count_infectious_bursts(grid, bursts):
    # holds the current amount of bursted caused an infection
    infectious_bursts = 0

    # expand grid
    for row in grid:
        for _ in range(1000):
            row.insert(0, False)
            row.append(False)

    for _ in range(1000):
        grid.insert(0, [False for _ in range(len(grid[0]))])
        grid.append([False for _ in range(len(grid[0]))])

    # holds the current direction
    direction = ABS_DIRECTIONS['up']
    # holds the current position
    position = (len(grid[0]) // 2, len(grid) // 2)

    for _ in range(bursts):
        current_node = grid[position[1]][position[0]]
        # change direction
        if current_node:
            direction = ABS_DIRECTIONS[REL_DIRECTIONS[direction]['right']]
        else:
            infectious_bursts += 1
            direction = ABS_DIRECTIONS[REL_DIRECTIONS[direction]['left']]

        grid[position[1]][position[0]] = not current_node
        position = position[0] + direction[0], position[1] + direction[1]

    return infectious_bursts


@pytest.mark.parametrize('input_file, bursts, expected_infectious_bursts', [
    (SAMPLE_INPUT, 70, 41),
    (SAMPLE_INPUT, 10_000, 5_587),
    # my puzzle input
    (MY_PUZZLE_INPUT, 10_000, 5_433)
])
def test_count_infectious_bursts(
        input_file, bursts, expected_infectious_bursts):
    """Test the solution"""
    # given
    with open(input_file) as f:
        grid = parse_map(f.read())

    # when
    actual_infectious_bursts = count_infectious_bursts(grid, bursts)

    # then
    assert actual_infectious_bursts == expected_infectious_bursts
