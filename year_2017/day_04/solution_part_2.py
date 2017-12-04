"""
Solution for the first puzzle of Day 4
"""

import os
from typing import List

import pytest

# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_input(raw_passphrases: str) -> List[List[str]]:
    """
    Parse the raw lines of passphrases and return
    a 2D list of the words of each passphrase.
    """
    return [l.split() for l in raw_passphrases.splitlines()]


def count_valid_passphrases(passphrases: List[List[str]]) -> int:
    """
    A new system policy has been put in place that requires all
    accounts to use a passphrase instead of simply a password.
    A passphrase consists of a series of
    words (lowercase letters) separated by spaces.

    To ensure security, a valid passphrase must contain no duplicate words.

    For example:

    * `aa bb cc dd ee` is valid.
    * `aa bb cc dd aa` is not valid - the word aa appears more than once.
    * `aa bb cc dd aaa` is valid - aa and aaa count as different words.

    The system's full passphrase list is available as your puzzle input.
    How many passphrases are valid?
    """
    return len([p for p in passphrases
                if len(p) == len(set(str(sorted(word)) for word in p))])


@pytest.mark.parametrize('passphrases, expected_valid', [
    ('abcde fghij', 1),
    ('abcde xyz ecdab', 0),
    ('a ab abc abd abf abj', 1),
    ('iiii oiii ooii oooi oooo', 1),
    ('oiii ioii iioi iiio', 0),
    ('abcde fghij\nabcde xyz ecdab\na ab abc abd abf abj\n'
     'iiii oiii ooii oooi oooo\noiii ioii iioi iiio\n', 3),
    # my puzzle input
    (open(MY_PUZZLE_INPUT).read(), 167)
])
def test_count_valid_passphrases(passphrases, expected_valid):
    """Test the solution"""
    # given
    parsed_input = parse_input(passphrases)

    # when
    actual_valid = count_valid_passphrases(parsed_input)

    # then
    assert actual_valid == expected_valid
