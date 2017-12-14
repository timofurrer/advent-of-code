"""
Solution for the first puzzle of Day 12
"""

import os

import pytest


# My puzzle input
SAMPLE_PUZZLE_INPUT = os.path.join(
        os.path.dirname(__file__), 'sample_input.txt')
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []

    def connected_with(self, other):
        if self.name == other.name:
            return True

        for neighbor in self.neighbors:
            if neighbor.connect_with(other):
                return True

        return False

    def all_endpoints(self, visited_endpoints=None):
        if visited_endpoints is None:
            visited_endpoints = []

        if self in visited_endpoints:
            return []

        endpoints = [self]
        for neighbor in self.neighbors:
            endpoints.extend(
                    neighbor.all_endpoints(visited_endpoints + endpoints))

        return endpoints


def parse_input(raw_programs):
    """
    Parse input and return sane data structure
    """
    programs = {}
    for l in raw_programs.splitlines():
        src, dest = l.split(' <-> ')
        if src not in programs:
            src_node = Node(src)
            programs[src] = src_node
        else:
            src_node = programs[src]

        for neighbor in (x.strip() for x in dest.split(',')):
            if neighbor not in programs:
                neighbor_node = Node(neighbor)
                programs[neighbor] = neighbor_node
            else:
                neighbor_node = programs[neighbor]

            src_node.neighbors.append(neighbor_node)

    return programs


def count_programs_in_group(programs, group) -> int:
    """
    Count the steps it takes to move to
    the given directions.
    """
    program_group = programs[group]
    return len(program_group.all_endpoints())


@pytest.mark.parametrize('input_file, group, expected_programs_in_group', [
    (SAMPLE_PUZZLE_INPUT, '0', 6),
    # my puzzle input
    (MY_PUZZLE_INPUT, '0', 130)
])
def test_count_programs_in_group(
        input_file, group, expected_programs_in_group):
    """Test the solution"""
    # given
    programs = parse_input(open(input_file).read())

    # when
    actual_programs_in_group = count_programs_in_group(programs, group)

    # then
    assert actual_programs_in_group == expected_programs_in_group
