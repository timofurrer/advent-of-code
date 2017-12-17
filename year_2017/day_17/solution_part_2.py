"""
Solution for the first puzzle of Day 17
"""

import pytest


# My puzzle input
MY_PUZZLE_INPUT = 301


def short_circut_spinlock(steps, reps=50_000_000):
    """
    Short-Circuit the spinlock
    """
    value_after_zero = None
    current_pos = 0
    for i in range(1, reps):
        current_pos = (current_pos + steps) % i + 1
        if current_pos == 1:
            value_after_zero = i

    return value_after_zero


@pytest.mark.parametrize('steps, expected_value', [
    # my puzzle input
    (MY_PUZZLE_INPUT, 33601318)
])
def test_short_circut_spinlock(steps, expected_value):
    """Test the solution"""
    # given & when
    actual_value = short_circut_spinlock(steps)

    # then
    assert actual_value == expected_value
