from Token import Token
from Production import Epsilon


class State:
    def __init__(self, num, transitions):
        self.num = num
        self.transitions = transitions

    def add_edge(self, label, next_state):
        self.transitions[label] = State(next_state, {})

    def get_next(self, p):
        return self.transitions[p]

    def __eq__(self, other):
        return self.num == other.num and self.transitions == other.transitions


class FSM:
    def __init__(self, production):
        self.name = production.non_terminal
        self.start = State(0, {})
        self.final = State(-1, {})
        self.add_productions(production)
        self.current_state = self.start

    def add_productions(self, production):
        self.name = production.non_terminal
        rhs_s = production.rhses
        count = 1
        for rhs in rhs_s:
            current = self.start
            for p in rhs[:-1]:
                current.add_edge(p, count)
                count += 1
                current = current.get_next(p)
            current.add_edge(rhs[-1], self.final.num)
            count += 1

    def change_state(self, p):
        self.current_state = self.current_state.get_next(p)

