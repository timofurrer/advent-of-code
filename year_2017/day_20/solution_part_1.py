"""
Solution for the first puzzle of Day 20
"""

import os
import re

import pytest


SAMPLE_INPUT = os.path.join(os.path.dirname(__file__), 'sample_input.txt')
# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Particle:
    def __init__(self, id, p, v, a):
        self.id = id
        self.p = p
        self.v = v
        self.a = a

    def tick(self):
        for i in range(3):
            self.v[i] += self.a[i]
            self.p[i] += self.v[i]

    def distance(self):
        return sum(abs(x) for x in self.p)

    def __repr__(self):
        return f'<Particle p={self.p}, v={self.v}, a={self.a}'


def parse_particles(raw_particles):
    particles = []
    for i, raw_particle in enumerate(raw_particles.splitlines()):
        p = [int(x) for x in re.search(
            r'p=<(.*?)>', raw_particle).group(1).split(',')]
        v = [int(x) for x in re.search(
            r'v=<(.*?)>', raw_particle).group(1).split(',')]
        a = [int(x) for x in re.search(
            r'a=<(.*?)>', raw_particle).group(1).split(',')]
        particles.append(Particle(i, p, v, a))
    return particles


def particle_closest_to_zero(particles):
    # simulating ticks
    for _ in range(500):
        for p in particles:
            p.tick()
    return min(particles, key=lambda p: p.distance()).id


@pytest.mark.parametrize('input_file, expected_particle', [
    (SAMPLE_INPUT, 0),
    # my puzzle input
    (MY_PUZZLE_INPUT, 125)
])
def test_particle_closest_to_zero(input_file, expected_particle):
    """Test the solution"""
    # given
    with open(input_file) as f:
        particles = parse_particles(f.read())

    # when
    actual_particle = particle_closest_to_zero(particles)

    # then
    assert actual_particle == expected_particle
