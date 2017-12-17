"""
Solution for the first puzzle of Day 17
"""

import pytest


# My puzzle input
MY_PUZZLE_INPUT = 301


def short_circut_spinlock(steps, reps=2018):
    """
    Short-Circuit the spinlock
    """
    values = [0]
    current_pos = 0
    for i in range(1, reps):
        current_pos = (current_pos + 1 + steps) % len(values)
        values.insert(current_pos + 1, i)

    return values[current_pos + 2]


@pytest.mark.parametrize('steps, expected_value', [
    (3, 638),
    # my puzzle input
    (MY_PUZZLE_INPUT, 1642)
])
def test_short_circut_spinlock(steps, expected_value):
    """Test the solution"""
    # given & when
    actual_value = short_circut_spinlock(steps)

    # then
    assert actual_value == expected_value
