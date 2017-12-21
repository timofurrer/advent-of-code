"""
Solution for the first puzzle of Day 21
"""

import os
import copy
from collections import namedtuple

import pytest

import numpy as np


SAMPLE_INPUT = os.path.join(os.path.dirname(__file__), 'sample_input.txt')
# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


Rule = namedtuple('Rule', ['pattern', 'to'])

BASE_GRID = [
    [False, True, False],
    [False, False, True],
    [True, True, True]
]


def parse_art_rules(raw_rules):
    rules = []
    for raw_rule in raw_rules.splitlines():
        raw_from, raw_to = raw_rule.split(' => ')
        rule_from, rule_to = [], []
        for r in raw_from.split('/'):
            rule_from.append([x == '#' for x in r])

        for r in raw_to.split('/'):
            rule_to.append([x == '#' for x in r])

        rule = Rule(rule_from, rule_to)
        rules.append(rule)
    return rules


def pattern_variations(pattern):
    patterns = [
        pattern.tolist(),
        np.flip(pattern, 0).tolist(),
        np.flip(pattern, 1).tolist(),
        np.rot90(pattern, k=1).tolist(),
        np.flip(np.rot90(pattern, k=1), 0).tolist(),
        np.rot90(pattern, k=2).tolist(),
        np.rot90(pattern, k=3).tolist(),
        np.flip(np.rot90(pattern, k=3), 0).tolist(),
    ]
    return patterns


def breakout_blocks(grid, size):
    hsplits = np.hsplit(np.array(grid), len(grid) // size)
    blocks = []
    for hsplit in hsplits:
        blocks.extend(np.vsplit(hsplit, len(grid) // size))
    return blocks


def merge_blocks(blocks, parts):
    # concatenate blocks into one grid
    vstacks = []
    for i in range(0, len(blocks), parts):
        vstack = np.vstack(blocks[i:i + parts])
        vstacks.append(vstack)
    return np.hstack(vstacks)


def create_pixel_art(rules, iterations):
    grid = copy.deepcopy(BASE_GRID)

    def match_rule(pattern):
        # calculate pattern rotations
        patterns = pattern_variations(pattern)

        for rule_pattern, rule_repl in rules:
            if rule_pattern in patterns:
                return rule_repl
        raise ValueError(f'No matching rule found for {pattern}')

    for _ in range(iterations):
        size = len(grid)
        if size % 2 == 0:
            blocksize = 2
        elif size % 3 == 0:
            blocksize = 3

        blocks = breakout_blocks(grid, blocksize)

        new_blocks = []
        for b in blocks:
            replacement = match_rule(b)
            new_blocks.append(replacement)

        grid = merge_blocks(new_blocks, size // blocksize)

    return grid


def count_pixels_on(rules, iterations):
    art = create_pixel_art(rules, iterations)

    pixels_on = 0
    for row in art:
        pixels_on += sum(int(c) for c in row)

    return pixels_on


@pytest.mark.parametrize('input_file, iterations, expected_pixels_on', [
    (SAMPLE_INPUT, 2, 12),
    # my puzzle input
    (MY_PUZZLE_INPUT, 5, 133)
])
def test_count_pixels_on(input_file, iterations, expected_pixels_on):
    """Test the solution"""
    # given
    with open(input_file) as f:
        rules = parse_art_rules(f.read())

    # when
    actual_pixels_on = count_pixels_on(rules, iterations=iterations)

    # then
    assert actual_pixels_on == expected_pixels_on
