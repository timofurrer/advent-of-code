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

    def connected_with(self, other, visited_endpoints=None):
        if visited_endpoints is None:
            visited_endpoints = []

        if self in visited_endpoints:
            return False

        if self.name == other.name:
            return True

        visited_endpoints.append(self)

        for neighbor in self.neighbors:
            if neighbor.connected_with(
                    other, visited_endpoints=visited_endpoints):
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


class Group:
    def __init__(self):
        self.nodes = set()

    def __contains__(self, node):
        return any(n for n in self.nodes if n.name == node.name)

    def add(self, node):
        self.nodes = set(list(self.nodes) + node.all_endpoints())


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


def count_groups(programs) -> int:
    """
    Count the steps it takes to move to
    the given directions.
    """
    groups = []
    for program in programs.values():
        for group in groups:
            if program in group:
                group.add(program)
                break
        else:
            group = Group()
            group.add(program)
            groups.append(group)

    return len(groups)


@pytest.mark.parametrize('input_file, expected_groups', [
    (SAMPLE_PUZZLE_INPUT, 2),
    # my puzzle input
    (MY_PUZZLE_INPUT, 189),
])
def test_count_groups(
        input_file, expected_groups):
    """Test the solution"""
    # given
    programs = parse_input(open(input_file).read())

    # when
    actual_groups = count_groups(programs)

    # then
    assert actual_groups == expected_groups
