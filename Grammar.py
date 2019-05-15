from functools import reduce
from copy import deepcopy
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

    def find_epsilon_none_terminals(self):
        epsilon_none_terminals = []
        for prod in self.prods.values():
            for sub_prod in prod.sub_prods:
                if len(sub_prod) == 1 and sub_prod[0] == "":
                    epsilon_none_terminals.append(prod.none_terminal)
                else:
                    for term in sub_prod:
                        pass #TODO

    def find_first_sets(self):
        pass

    def find_follow_sets(self):
        pass

    def make_LL1_dfa(self):
        pass

    @staticmethod
    def make_grammar(self, compressed_prods):
        non_terminals = []
        for c_prod in compressed_prods:
            for prod in c_prod[1:]:
                r = prod(c_prod[0], prod)


