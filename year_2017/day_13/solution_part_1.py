"""
Solution for the first puzzle of Day 13
"""

import os

import pytest


# My puzzle input
SAMPLE_PUZZLE_INPUT = os.path.join(
        os.path.dirname(__file__), 'sample_input.txt')
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Firewall:
    def __init__(self, id_, range_):
        self.id = id_
        self.range = range_
        self.current_pos = 0
        self.moving_direction = 1

    def move_scanner(self):
        self.current_pos = self.current_pos + self.moving_direction
        if self.moving_direction > 0 and self.current_pos + 1 == self.range:
            self.moving_direction = -1
        elif self.current_pos == 0:
            self.moving_direction = 1

    @property
    def severity(self):
        return self.id * self.range


def parse_input(raw_firewalls):
    """
    Parse input and return sane data structure
    """
    firewalls = {}
    for f in raw_firewalls.splitlines():
        id_, range_ = [int(x) for x in f.split(': ')]
        firewalls[id_] = Firewall(id_, range_)
    return firewalls


def calculate_trip_severity(firewalls) -> int:
    """
    Calculate the severity of a trip given the firewall
    """
    severity = 0
    picoseconds = max(f.id for f in firewalls.values()) + 1
    for current_pos in range(picoseconds):
        if current_pos in firewalls:
            current_firewall = firewalls[current_pos]
            if current_firewall.current_pos == 0:
                # caught
                severity += current_firewall.severity
        # move scanners
        for f in firewalls.values():
            f.move_scanner()

    return severity


@pytest.mark.parametrize('input_file, expected_trip_severity', [
    (SAMPLE_PUZZLE_INPUT, 24),
    # my puzzle input
    (MY_PUZZLE_INPUT, 748)
])
def test_calculate_trip_severity(input_file, expected_trip_severity):
    """Test the solution"""
    # given
    firewalls = parse_input(open(input_file).read())

    # when
    actual_trip_severity = calculate_trip_severity(firewalls)

    # then
    assert actual_trip_severity == expected_trip_severity
