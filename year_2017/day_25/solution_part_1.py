"""
Solution for the first puzzle of Day 25
"""

import os
import re
from collections import defaultdict

import pytest


SAMPLE_INPUT = os.path.join(os.path.dirname(__file__), 'sample_input.txt')
# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_blueprint(raw_blueprint):
    blueprint_lines = raw_blueprint.splitlines()
    begin_state = re.search(r'Begin in state ([A-F])',
                            blueprint_lines[0]).group(1)
    steps = int(re.search(r'Perform a diagnostic checksum after (\d+) steps.',
                          blueprint_lines[1]).group(1))

    states = defaultdict(dict)
    current_state = None
    current_if = None

    for state_line in (l.strip() for l in blueprint_lines[3:]):
        if not state_line:
            continue

        start_match = re.search(r'In state ([A-F]):', state_line)
        if start_match:
            current_state = start_match.group(1)
            continue

        if_match = re.search(r'If the current value is (\d):', state_line)
        if if_match:
            current_if = int(if_match.group(1))
            states[current_state][current_if] = {}
            continue

        write_match = re.search(r'- Write the value (\d).', state_line)
        if write_match:
            states[current_state][current_if]['value'] = int(
                    write_match.group(1))

        cur_match = re.search(
                r'- Move one slot to the (right|left).', state_line)
        if cur_match:
            cursor_dir = 1 if cur_match.group(1) == 'right' else -1
            states[current_state][current_if]['move'] = cursor_dir

        next_match = re.search(r'- Continue with state ([A-F]).', state_line)
        if next_match:
            states[current_state][current_if]['next'] = next_match.group(1)

    return begin_state, steps, states


def turing_machine_checksum(blueprint):
    begin_state, steps, states = blueprint

    tape = [0 for _ in range(5_000)]
    cursor = len(tape) // 2
    state = begin_state

    for _ in range(steps):
        current_state = states[state]
        current_action = current_state[tape[cursor]]
        tape[cursor] = current_action['value']
        cursor = cursor + current_action['move']
        state = current_action['next']

    return sum(tape)


@pytest.mark.parametrize('input_file, expected_checksum', [
    (SAMPLE_INPUT, 3),
    # my puzzle input
    (MY_PUZZLE_INPUT, 2794)
])
def test_turing_machine_checksum(input_file, expected_checksum):
    """Test the solution"""
    # given
    with open(input_file) as f:
        blueprint = parse_blueprint(f.read())

    # when
    actual_checksum = turing_machine_checksum(blueprint)

    # then
    assert actual_checksum == expected_checksum
