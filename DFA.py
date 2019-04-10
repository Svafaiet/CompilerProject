import string
from enum import Enum



class TOKEN(Enum):
    NUM = "NUM"
    KEYWORD = "KEYWORD"
    ID = "ID"
    SYMBOL = "SYMBOL"
    COMMENT = "COMMENT"
    WHITE_SPACE = "WHITESPACE"
    EOF = "EOF"


class State:
    def __init__(self, last_successor=None, goal_type=None):
        self.successors = dict()
        self.last_successor = last_successor
        self.goal_type = goal_type

    def get_next_state(self, value):
        if value in self.successors:
            return self.successors[value]
        else:
            return self.last_successor

    def add_successor(self, other_state, edge_values):
        for value in edge_values:
            if not (value in self.successors):
                self.successors[value] = other_state


class DFA:
    white_spaces = tuple(map(chr, [32, 10, 13, 9, 11, 12]))

    def __init__(self, init_state, states):
        self.states = states
        self.init_state = init_state

    @staticmethod
    def make_dfa(states, edges):
        """
            for making a new state add (state_name, goal_type, last_successor_name) to collection and pass it to DFAMaker
            first state will be initial state in dfa
            goal_type and last_successor_name are not required
            for edges do it in form (edge_first_state_name, edge_sec_state_name, set_of_available_values)
        """
        if len(states) == 0:
            raise Exception("can not have empty dfa")

        init_state_name = states[0]

        name_to_state = dict()
        for state in states:
            if not (state[0] in states):
                name_to_state[state[0]] = State()

        for state in states:
            if len(state) > 1:
                name_to_state[state[0]].goal_type = state[1]
            if len(state) > 2:
                name_to_state[state[0]].last_successor = name_to_state[state[2]]

        for edge in edges:
            name_to_state[edge[0]].add_successor(name_to_state[edge[1]], edge[2])

        return DFA(name_to_state[init_state_name], list(name_to_state.values()))


    # todo


