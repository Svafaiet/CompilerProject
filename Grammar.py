from Production import epsilon, Production


class Grammar:
    def __init__(self, prods):
        self.prods = None
        self.make_prods(prods)

    def make_prods(self, prods):
        self.prods = dict()
        for prod in prods:
            self.prods[prod.non_terminal] = prod

    def left_factorize_prods(self):
        new_prods = []
        for prod in self.prods:
            new_prods += prod.left_factorize()
        self.make_prods(new_prods)

    def remove_left_recursion(self):
        non_terminals = list(self.prods.keys())
        for i, non_terminal in enumerate(non_terminals):
            grammar_changed = True
            while grammar_changed:
                grammar_changed = False
                rhs_i = self.prods[non_terminal].rhss
                for rhs in rhs_i:
                    for A_j in non_terminals[:i]:
                        if rhs[0] == A_j:
                            rhs_revised = rhs[1:]
                            self.prods[non_terminal].rhss.remove(rhs)
                            grammar_changed = True
                            for prod in self.prods[A_j].rhss:
                                self.prods[non_terminal].rhss.append(prod + rhs_revised)

            alpha_set = [prod[1:] for prod in self.prods[non_terminal].rhss if prod[0] == non_terminal]
            beta_set = [prod for prod in self.prods[non_terminal].rhss if prod[0] != non_terminal]
            if len(alpha_set) > 0:
                self.prods.pop(non_terminal)
                non_terminal_new = non_terminal + '_new'
                self.prods[non_terminal] = Production(non_terminal, [
                    beta_i + [non_terminal_new] if beta_i != [epsilon] else [non_terminal_new] for beta_i in beta_set])
                self.prods[non_terminal_new] = Production(non_terminal_new,
                                                          [alpha_i + [non_terminal_new] for alpha_i in alpha_set])
                self.prods[non_terminal_new].rhss += [[epsilon]]

    def find_epsilon_non_terminals(self):
        epsilon_non_terminals = []
        for prod in self.prods.values():
            for sub_prod in prod.sub_prods:
                if len(sub_prod) == 1 and sub_prod[0] == "":
                    epsilon_non_terminals.append(prod.none_terminal)
                else:
                    for term in sub_prod:
                        pass  # TODO

    def make_first_sets(self):
        pass

    def make_follow_sets(self):
        pass

    def make_grammar_ll1(self):
        self.remove_left_recursion()
        self.left_factorize_prods()
        self.find_epsilon_non_terminals()
        self.make_first_sets()
        self.make_follow_sets()

    @staticmethod
    def make_grammar(compressed_prods):
        productions = []
        for c_prod in compressed_prods:
            r = Production(c_prod[0], c_prod[1:])
            productions.append(r)
        return Grammar(productions)
