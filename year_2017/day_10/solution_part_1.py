"""
Solution for the first puzzle of Day 10
"""

import pytest

# My puzzle input
MY_PUZZLE_INPUT = [
    106, 118, 236, 1, 130, 0, 235, 254,
    59, 205, 2, 87, 129, 25, 255, 118
]


def build_hash(input_list, lengths):
    """
    Build hash for the given list
    """
    current_position = 0
    skip_size = 0

    list_len = len(input_list)
    for current_length in lengths:
        # calculate end index
        end_position = (current_position + current_length - 1) % list_len

        # reverse sublist
        if end_position + 1 >= current_position:
            # no wrapping
            input_list[current_position:end_position + 1] = reversed(
                    input_list[current_position:end_position + 1])
        else:
            # wrapping
            until_end_len = len(input_list) - current_position

            reversed_sublist = list(reversed(
                input_list[current_position:] + input_list[:end_position + 1]))

            input_list[current_position:] = reversed_sublist[:until_end_len]
            input_list[:end_position + 1] = reversed_sublist[until_end_len:]

        # move current position
        current_position = (
                current_position + current_length + skip_size) % list_len

        # increase skip size
        skip_size += 1

    return input_list[0] * input_list[1]


@pytest.mark.parametrize('input_list, lengths, expected_hash', [
    ([0, 1, 2, 3, 4], [3, 4, 1, 5], 12),
    # my puzzle input
    (list(range(256)), MY_PUZZLE_INPUT, 6909)
])
def test_build_hash(input_list, lengths, expected_hash):
    """Test the solution"""
    # given & when
    actual_hash = build_hash(input_list, lengths)

    # then
    assert actual_hash == expected_hash
