import string

class State:
    def __init__(self, last_successor, goal_type=None):
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
    def __init__(self, init_state, states):
        self.states = states
        self.init_state = init_state

    @staticmethod
    def make_dfa(states, edges):
        """
            for making a new state add (state_name, last_successor_name, goal_type) to collection and pass it to DFAMaker
            first state will be initial state in dfa
            for edges do it in form (edge_first_state_name, edge_sec_state_name, set_of_available_values)
        """
        if len(states) == 0:
            raise Exception("can not have empty dfa")

        init_state_name = states[0]

        name_to_state = dict()
        for state in states:
            name_to_state[state[0]] = State(None, state[2])
        for state in states:
            name_to_state[state[0]].last_successor = name_to_state[state[1]]

        for edge in edges:
            name_to_state[edge[0]].add_successor(name_to_state[edge[1]], edge[2])

        return DFA(name_to_state[init_state_name], list(name_to_state.values()))


    # todo


digits = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
chars = tuple(string.ascii_lowercase) + tuple(string.ascii_uppercase)
ws = tuple(map(chr, [32, 10, 13, 9, 11, 12]))
symbols = ';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<'

print(chars)
