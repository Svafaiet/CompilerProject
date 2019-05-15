from functools import reduce
from copy import deepcopy


class Grammar:
    def __init__(self, prods):
        self.prods = None
        self.make_prods(prods)

    def make_prods(self, prods):
        self.prods = dict()
        for prod in prods:
            self.prods[prod.none_terminal] = prod

    def left_factorize_prods(self):
        new_prods = []
        for prod in self.prods:
            new_prods += prod.left_factorize()
        self.make_prods(new_prods)

    def remove_left_recursion(self):
        pass

    def find_ebsilon_none_terminals(self):
        ebsilon_none_terminals = []
        for prod in self.prods.values():
            for sub_prod in prod.sub_prods:
                if len(sub_prod) == 1 and sub_prod[0] == "":
                    ebsilon_none_terminals.append(prod.none_terminal)
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


        none_terminals = []

        for c_prod in compressed_prods:
            for prod in c_prod[1:]:
                r = prod(c_prod[0], prod)


