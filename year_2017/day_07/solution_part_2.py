"""
Solution for the first puzzle of Day 4
"""

import os
import re
from collections import namedtuple
from typing import Tuple, List

import pytest

# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


Program = namedtuple('Program', ['name', 'weight'])


def parse_input(raw_programs: str) -> dict:
    """
    Parse tower input
    """
    programs = {}
    for raw_program in raw_programs.splitlines():
        name = raw_program.split()[0]
        weight = re.search(r'\((\d+)\)', raw_program).group(1)
        program = Program(name, weight)
        if '->' in raw_program:
            sub_programs = raw_program.split('->', maxsplit=1)[-1]
            programs[program] = [
                    Program(x, 0) for x in sub_programs.strip().split(', ')]
        else:
            programs[program] = []

    return programs


class Node:
    def __init__(self, name, weight):
        self.name = name
        self.weight = int(weight)
        self.nodes = []

    def __str__(self):
        return '<Node {0} ({1}) -> {2}>'.format(
                self.name, self.weight, [str(x) for x in self.nodes])

    __repr__ = __str__

    @property
    def total_weight(self):
        return self.weight + sum(x.total_weight for x in self.nodes)

    @property
    def is_unbalanced(self):
        return len(set([x.total_weight for x in self.nodes])) != 1

    @property
    def has_only_leafs(self):
        return sum(len(x.nodes) for x in self.nodes) == 0

    def get_unbalanced(self):
        if self.is_unbalanced:
            for n in self.nodes:
                unbalanced = n.get_unbalanced()
                if unbalanced:
                    return unbalanced

        if self.is_unbalanced:
            return self.nodes

        return None


def find_root_program(programs: dict) -> Tuple[Node, List]:
    """
    Find the root program
    """
    # holds all nodes which are not a leaf
    nodes = {k: v for k, v in programs.items() if len(v) > 0}
    for program, sub_programs in nodes.items():
        if program.name not in (p.name for sp in nodes.values() for p in sp):
            return Node(program.name, program.weight), sub_programs

    return None


def build_subtree(root, sub_programs, programs):
    """
    Build subtree
    """
    for node in sub_programs:
        # find node in programs
        program = [
                (p, s) for p, s in programs.items() if p.name == node.name][0]

        program_node = Node(program[0].name, program[0].weight)
        if len(program[1]) > 0:
            program_node = build_subtree(program_node, program[1], programs)

        root.nodes.append(program_node)

    return root


def build_tree(programs: dict) -> Node:
    """
    Find the root program
    """
    # holds all nodes which are not a leaf
    root, sub_programs = find_root_program(programs)
    return build_subtree(root, sub_programs, programs)


def find_unbalanced_dics(programs: dict) -> Tuple[str, int]:
    """
    Find the unbalanced disc and return its name
    and the weight it should have
    """
    tree = build_tree(programs)

    unbalanced = tree.get_unbalanced()
    haviest = max(unbalanced, key=lambda x: x.total_weight)
    lightest = min(unbalanced, key=lambda x: x.total_weight)
    diff = haviest.total_weight - lightest.total_weight

    # return None
    return haviest.name, haviest.weight - diff


@pytest.mark.parametrize('programs, expected_unbalanced_disc', [
    (open(os.path.join(os.path.dirname(__file__),
                       'sample_input.txt')).read(), ('ugml', 60)),
    # my puzzle input
    (open(MY_PUZZLE_INPUT).read(), ('ltleg', 802))
])
def test_find_unbalanced_dics(programs, expected_unbalanced_disc):
    """Test the solution"""
    # given
    parsed_input = parse_input(programs)

    # when
    actual_unbalanced_disc = find_unbalanced_dics(parsed_input)

    # then
    assert actual_unbalanced_disc == expected_unbalanced_disc
