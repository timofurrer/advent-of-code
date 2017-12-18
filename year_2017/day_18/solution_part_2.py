"""
Solution for the first puzzle of Day 18
"""

import os
from queue import Queue
from collections import defaultdict

import pytest


SAMPLE_INPUT = os.path.join(os.path.dirname(__file__), 'sample_input_2.txt')
# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_instructions(raw_instructions):
    instructions = []
    for raw_instruction in raw_instructions.splitlines():
        instructions.append(raw_instruction.split())
    return instructions


def is_number(x):
    try:
        int(x)
    except ValueError:
        return False
    else:
        return True


def run(program_id, instructions, send_queue, recv_queue):
    registers = defaultdict(int)
    registers['p'] = program_id

    def reg_value(x):
        return int(x) if is_number(x) else registers[x]

    sent = 0
    received = 0

    i = 0
    while i < len(instructions):
        instruction, *arguments = instructions[i]
        if instruction == 'snd':
            send_queue.put(registers[arguments[0]])
            sent += 1
        elif instruction == 'set':
            X, Y = arguments
            registers[X] = reg_value(Y)
        elif instruction == 'add':
            X, Y = arguments
            registers[X] += reg_value(Y)
        elif instruction == 'mul':
            X, Y = arguments
            registers[X] *= reg_value(Y)
        elif instruction == 'mod':
            X, Y = arguments
            registers[X] %= reg_value(Y)
        elif instruction == 'rcv':
            if recv_queue.empty():
                # can read from queue -> maybe deadlocked?
                yield False, sent, received
                continue
            else:
                registers[arguments[0]] = recv_queue.get_nowait()
                received += 1
        elif instruction == 'jgz':
            X, Y = arguments
            if reg_value(X) > 0:
                i += reg_value(Y)
                continue
        else:
            raise ValueError(f'unknown instruction {instruction}')

        i += 1
        yield True, sent, received

    return None, sent, received


def communicate(instructions):
    a_queue = Queue()
    b_queue = Queue()

    program_a = run(0, instructions, b_queue, a_queue)
    program_b = run(1, instructions, a_queue, b_queue)

    while True:
        a_can_receive, a_sent, a_received = next(program_a)
        b_can_receive, b_sent, b_received = next(program_b)

        if not a_can_receive and not b_can_receive:
            return a_sent, b_sent


@pytest.mark.parametrize('input_file, expected_program_b_sent', [
    (SAMPLE_INPUT, 3),
    # my puzzle input
    (MY_PUZZLE_INPUT, 8001)
])
def test_communicate(input_file, expected_program_b_sent):
    """Test the solution"""
    # given
    with open(input_file) as f:
        instructions = parse_instructions(f.read())

    # when
    actual_program_a_sent, actual_program_b_sent = communicate(instructions)

    # then
    assert actual_program_b_sent == expected_program_b_sent
