"""
Solution for the first puzzle of Day 24
"""

import os
from collections import defaultdict

import pytest


SAMPLE_INPUT = os.path.join(os.path.dirname(__file__), 'sample_input.txt')
# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_components(raw_components):
    components = defaultdict(set)
    for raw_component in raw_components.splitlines():
        a, b = [int(x) for x in raw_component.split('/')]
        components[a].add(b)
        components[b].add(a)
    return components


def build_bridges(bridge, components):
    current_endport = bridge[-1][1]
    for port in components[current_endport]:
        # check if component: (current_endport, port) is not
        # yet a variations of a component in the current bridge
        if (current_endport, port) not in bridge \
                and (port, current_endport) not in bridge:
            # append new component to bridge
            current_bridge = bridge + [(current_endport, port)]
            # yield entire bridge
            yield from build_bridges(current_bridge, components)
            # every stage of a bridge is a bridge itself!
            yield current_bridge


def evaluate_strongest_bridge(components, start_bridge):
    bridges = []
    for bridge in build_bridges(start_bridge, components):
        strength = sum(a + b for a, b in bridge)
        bridges.append(strength)
    return max(bridges)


@pytest.mark.parametrize('input_file, start_bridge, expected_max_strength', [
    (SAMPLE_INPUT, [(0, 0)], 31),
    # my puzzle input
    (MY_PUZZLE_INPUT, [(0, 0)], 1906)
])
def test_evaluate_strongest_bridge(
        input_file, start_bridge, expected_max_strength):
    """Test the solution"""
    # given
    with open(input_file) as f:
        components = parse_components(f.read())

    # when
    actual_max_strength = evaluate_strongest_bridge(components, start_bridge)

    # then
    assert actual_max_strength == expected_max_strength
