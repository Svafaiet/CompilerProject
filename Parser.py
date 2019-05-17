from Grammar import Grammar
from FSM import FSM
from Production import epsilon


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.state_diagram = dict()
        self.build_state_diagram()
        self.current_fsm = self.state_diagram[self.grammar.start_symbol]
        self.stack = []

    def build_state_diagram(self):
        for production in self.grammar.prods:
            self.state_diagram[production.non_terminal] = FSM(production)

    def parse(self, next_token):
        """
        :param next_token: next input token
        :return: a tuple (error_state, next_token_needed)
        """
        curr = self.current_fsm.current_state
        if next_token in curr.transitions:
            self.current_fsm.change_state(next_token)
            if self.current_fsm.current_state == self.current_fsm.final:
                self.final_state_proc()
            return False, True
        else:
            for edge in curr.transitions:
                if next_token in self.grammar.first_sets(edge) or \
                        (epsilon in self.grammar.first_sets(edge) and next_token in self.grammar.follow_sets(edge)):
                    self.non_terminal_proc(edge)
                    self.current_fsm = self.state_diagram[edge]
                    self.current_fsm.current_state = self.current_fsm.start
                    return False, False
                elif edge == epsilon and next_token in self.grammar.follow_sets(self.current_fsm.name):
                    self.final_state_proc()
                    return False, False

    def non_terminal_proc(self, edge):
        fsm = self.current_fsm
        fsm.change_state(edge)
        self.stack.append(fsm)
        return

    def final_state_proc(self):
        try:
            fsm = self.stack.pop(-1)
            while fsm.current_state == fsm.final:
                fsm = self.stack.pop(-1)
            self.current_fsm = fsm
            return
        except IndexError:
            return
