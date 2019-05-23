from Grammar import Grammar
from FSM import FSM
from ParseTree import ParseTree
from Production import epsilon
import copy
from Token import CTokenType, Token


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.state_diagram = dict()
        self.build_state_diagram()
        self.current_fsm = self.state_diagram[self.grammar.grammar.start_symbol]
        self.stack = []
        self.parse_tree = ParseTree()

    def build_state_diagram(self):
        for prod in self.grammar.grammar.prods:
            production = self.grammar.grammar.prods[prod]
            self.state_diagram[production.non_terminal] = FSM(production)

    def parse(self, next_token):
        """
        :param next_token: next input token
        :return: a tuple (error_state, next_token_needed)
        """
        curr = self.current_fsm.current_state
        if next_token in curr.transitions:
            self.current_fsm.change_state(next_token)
            self.parse_tree.iterate(next_token)
            if self.current_fsm.current_state == self.current_fsm.final:
                self.final_state_proc()
            return False, True, None
        elif self.is_valid(next_token):
            for edge in curr.transitions:
                if isinstance(edge, str):
                    if next_token in self.grammar.first_sets[edge] or edge in self.grammar.epsilons and \
                            next_token in self.grammar.follow_sets[edge]:
                        if curr == self.current_fsm.start:
                            self.parse_tree.insert_rhs(self.get_rhs(next_token))
                        self.non_terminal_proc(edge)
                        self.current_fsm = self.state_diagram[edge]
                        self.current_fsm.current_state = self.current_fsm.start
                        return False, False, None
                elif edge == epsilon[0] and next_token in self.grammar.follow_sets[self.current_fsm.name]:
                    self.final_state_proc()
                    self.parse_tree.insert_rhs(epsilon)
                    return False, False, None
        else:
            eof = Token(CTokenType.EOF)
            if next_token == eof:
                return True, False, (3, next_token)
            elif eof in curr.transitions:
                return True, False, (4, next_token)
            else:
                for edge in curr.transitions:
                    if isinstance(edge, str):
                        if next_token in self.grammar.follow_sets[edge]:
                            self.current_fsm.change_state(edge)
                            if self.current_fsm.current_state == self.current_fsm.final:
                                self.final_state_proc()
                            return True, True, (2, edge)
                        else:
                            return True, True, (1, next_token)
                    else:
                        self.current_fsm.change_state(edge)
                        if self.current_fsm.current_state == self.current_fsm.final:
                            self.final_state_proc()
                        return True, False, (0, edge)

    def non_terminal_proc(self, edge):
        fsm = copy.copy(self.current_fsm)
        fsm.change_state(edge)
        self.stack.append(fsm)
        return

    def final_state_proc(self):
        try:
            fsm = self.stack.pop(-1)
            self.current_fsm = fsm
            while fsm.current_state == fsm.final:
                fsm = self.stack.pop(-1)
            self.current_fsm = fsm
            return
        except IndexError:
            return

    def is_valid(self, next_token):
        curr = self.current_fsm.current_state
        for edge in curr.transitions:
            if isinstance(edge, str):
                if next_token in self.grammar.first_sets[edge] or edge in self.grammar.epsilons and \
                        next_token in self.grammar.follow_sets[edge]:
                    return True
            elif edge == epsilon[0] and next_token in self.grammar.follow_sets[self.current_fsm.name]:
                return True
        return False

    def get_rhs(self, next_token):
        production = self.grammar.grammar.prods[self.current_fsm.name]
        for rhs in production.rhses:
            if isinstance(rhs[0], str):
                if next_token in self.grammar.first_sets[rhs[0]] or rhs[0] in self.grammar.epsilons and \
                        next_token in self.grammar.follow_sets[rhs[0]]:
                    return rhs
            else:
                if next_token == rhs[0]:
                    return rhs
