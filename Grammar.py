from functools import reduce
from copy import deepcopy

from Directive import Directive
from Token import Token
from Production import epsilon


class Grammar:
    def __init__(self, prods):
        self.prods = None
        self.make_prods(prods)

    def make_prods(self, prods):
        self.prods = dict()
        for prod in prods:
            ## TODO why prod??
            self.prods[prod.non_terminal] = prod

    @staticmethod
    def make_grammar(compressed_prods):

        none_terminals = []

        for c_prod in compressed_prods:
            for prod in c_prod[1:]:
                r = prod(c_prod[0], prod)

    def left_factorize_prods(self):
        new_prods = []
        for prod in self.prods:
            new_prods += prod.left_factorize()
        self.make_prods(new_prods)

    def remove_left_recursion(self):
        non_terminals = self.prods.keys()
        for i, non_terminal in non_terminals:
            grammar_changed = True
            while grammar_changed:
                grammar_changed = False
                rhs_i = self.prods[non_terminal]
                for rhs in rhs_i:
                    for A_j in non_terminals[:i]:
                        if rhs[0] == A_j:
                            rhs_revised = rhs[1:]
                            self.prods[non_terminal].remove(rhs)
                            grammar_changed = True
                            for prod in self.prods[A_j]:
                                self.prods[non_terminal].append(prod + rhs_revised)

            alpha_set = [prod[1:] for prod in self.prods[non_terminal] if prod[0] == non_terminal]
            beta_set = [prod for prod in self.prods[non_terminal] if prod[0] != non_terminal]
            self.prods.pop(non_terminal)
            non_terminal_new = non_terminal.join("_new")
            self.prods[non_terminal] = [[beta_i + non_terminal_new] for beta_i in beta_set]
            self.prods[non_terminal_new] = [[alpha_i + non_terminal_new] for alpha_i in alpha_set]
            self.prods[non_terminal_new] += [epsilon]


class LL1Grammar:
    def __init__(self, grammar):
        self.grammar = grammar
        self.grammar.left_factorize_prods()
        self.grammar.remove_left_recursion()
        self.epsilons = list()
        self.first_sets = dict()
        self.follow_sets = dict()
        self.find_epsilon_none_terminals()
        self.make_first_sets()
        self.make_follow_sets()

    def find_epsilon_none_terminals(self):
        self.epsilons = list()
        for prod in self.grammar.prods.values():
            if epsilon in prod.rhses:
                self.epsilons.append(prod.none_terminal)
        epsilons_changed = True
        while epsilons_changed:
            epsilons_changed = False
            for prod in self.grammar.prods.values():
                if not ((prod.none_terminal in self.epsilons) or any(isinstance(rhs, Token) for rhs in prod.rhses)):
                    for rhs in prod.rhses:
                        if all((isinstance(value, Directive) or value in self.epsilons) for value in rhs):
                            epsilons_changed = True
                            self.epsilons.append(prod.none_terminal)
                            break

    def make_first_sets(self):
        for none_terminal in self.grammar.prods.keys():
            self.first_sets[none_terminal] = dict()
        grammar_changed = True
        while grammar_changed:
            grammar_changed = False
            for prod in self.grammar.prods.values():
                for rhs in prod.rhses:
                    if not (rhs is epsilon):
                        for value in rhs:
                            if isinstance(value, Token):
                                if not (value in self.first_sets[prod.none_terminal]):
                                    self.first_sets[prod.none_terminal][value] = rhs
                                    grammar_changed = True
                            elif not isinstance(value, Directive):
                                for token in self.first_sets[value]:
                                    if not (token in self.first_sets[prod.none_terminal]):
                                        self.first_sets[prod.none_terminal][token] = rhs
                                        grammar_changed = True
                            if not ((value in self.epsilons) or (isinstance(value, Directive))):
                                break

    def make_follow_sets(self):
        for none_terminal in self.grammar.prods.keys():
            self.follow_sets[none_terminal] = dict()
        #TODO