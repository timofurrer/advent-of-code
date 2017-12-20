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


def simulate_particles(particles):
    # simulating ticks
    for _ in range(500):
        updated, collided = [], []
        for p in particles:
            p.tick()
            colliding_particles = [x for x in updated if x.p == p.p]
            if colliding_particles:
                collided.extend(colliding_particles + [p])
            updated.append(p)
        particles = [x for x in particles if x not in collided]
    return particles


@pytest.mark.parametrize('input_file, expected_survived_particles', [
    # my puzzle input
    (MY_PUZZLE_INPUT, 461)
])
def test_simulate_particles(input_file, expected_survived_particles):
    """Test the solution"""
    # given
    with open(input_file) as f:
        particles = parse_particles(f.read())

    # when
    actual_survived_particles = len(simulate_particles(particles))

    # then
    assert actual_survived_particles == expected_survived_particles
