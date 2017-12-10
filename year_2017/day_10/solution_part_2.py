"""
Solution for the second puzzle of Day 10
"""

import operator
import functools

import pytest

# My puzzle input
MY_PUZZLE_INPUT = '106,118,236,1,130,0,235,254,59,205,2,87,129,25,255,118'


def knothash(string, rounds=64, stdsuffix=[17, 31, 73, 47, 23],
             hash_len=256, block_size=16):
    """
    Build knothash
    """
    # initialize hash length
    sparse_hash = list(range(hash_len))

    # convert string to ASCII bytes sequence
    lengths = [ord(c) for c in string] + stdsuffix

    # initial values
    current_position = 0
    skip_size = 0

    for _ in range(rounds):
        for current_length in lengths:
            # calculate end index
            end_position = (current_position + current_length - 1) % hash_len

            # reverse sublist
            if end_position + 1 >= current_position:
                # no wrapping
                sparse_hash[current_position:end_position + 1] = reversed(
                        sparse_hash[current_position:end_position + 1])
            else:
                # wrapping
                until_end_len = len(sparse_hash) - current_position

                reversed_sublist = list(reversed(
                    sparse_hash[current_position:] +
                    sparse_hash[:end_position + 1]))

                sparse_hash[current_position:] = reversed_sublist[:until_end_len]
                sparse_hash[:end_position + 1] = reversed_sublist[until_end_len:]

            # move current position
            current_position = (
                    current_position + current_length + skip_size) % hash_len

            # increase skip size
            skip_size += 1

    # construct dense hash from sparse hash
    dense_hash_blocks = []
    for i in range(0, len(sparse_hash), block_size):
        block = functools.reduce(
                operator.xor, sparse_hash[i:i + block_size], 0)
        dense_hash_blocks.append(block)

    dense_hash = ''.join('{:02x}'.format(c) for c in dense_hash_blocks)
    return dense_hash


@pytest.mark.parametrize('string, expected_hash', [
    ('', 'a2582a3a0e66e6e86e3812dcb672a272'),
    ('AoC 2017', '33efeb34ea91902bb2f59c9920caa6cd'),
    ('1,2,3', '3efbe78a8d82f29979031a4aa0b16a9d'),
    ('1,2,4', '63960835bcdc130f0b66d7ff4f6a5a8e'),
    # my puzzle input
    (MY_PUZZLE_INPUT, '9d5f4561367d379cfbf04f8c471c0095')
])
def test_knothash(string, expected_hash):
    """Test the solution"""
    # given & when
    actual_hash = knothash(string)

    # then
    assert actual_hash == expected_hash
