from copy import deepcopy
from functools import reduce


class Epsilon:
    def __hash__(self):
        return hash("epsilon")

    def __eq__(self, other):
        return isinstance(other, Epsilon)

    def __str__(self):
        return "__EPSILON__"

epsilon = [Epsilon()]


class Production:
    def __init__(self, non_terminal, rhses):
        self.non_terminal = non_terminal
        self.rhses = rhses
