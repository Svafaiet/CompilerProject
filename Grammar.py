from functools import reduce

from Directive import Directive
from Production import epsilon, Production
from Token import Token


class Grammar:
    def __init__(self, prods, start):
        self.prods = None
        self.make_prods(prods)
        self.start_symbol = start

    def make_prods(self, prods):
        self.prods = dict()
        for prod in prods:
            self.prods[prod.non_terminal] = prod

    def left_factorize_prods(self):
        grammar_changed = True
        unchecked_prods = list(self.prods.values())
        new_prods = []
        while grammar_changed:
            grammar_changed = False
            for prod in list(unchecked_prods):
                index = 0
                prefix = []
                while True:
                    if any((len(rhs) <= index or rhs == epsilon) for rhs in prod.rhses):
                        break
                    if all(ith_term == prod.rhses[0][index] for ith_term in list(rhs[index] for rhs in prod.rhses)):
                        prefix.append(prod.rhses[0][index])
                        index += 1
                    else:
                        break
                unchecked_prods.remove(prod)
                if index > 0:
                    prefix_name = reduce(lambda str1, str2: str(str1) + str(str2), prefix)
                    suffix_name = prod.non_terminal + "." + str(prefix_name)
                    new_prods.append(Production(prod.non_terminal, [prefix + [suffix_name]]))
                    new_rhses = list((epsilon if len(rhs) <= index else rhs[index:]) for rhs in prod.rhses)
                    unchecked_prods.append(Production(suffix_name, new_rhses))
                    grammar_changed = True
                else:
                    groups = dict()
                    for rhs in prod.rhses:
                        if rhs != epsilon:
                            if not (rhs[0] in groups):
                                groups[rhs[0]] = []
                            groups[rhs[0]].append(rhs)
                        else:
                            groups[epsilon[0]] = [epsilon]
                    if len(groups) == len(prod.rhses):
                        new_prods.append(prod)
                    else:
                        new_rhses = []
                        for term in groups:
                            if term == epsilon[0]:
                                new_rhses.append(epsilon)
                            elif len(groups[term]) == 1:
                                new_rhses.append(groups[term][0])
                            else:
                                new_prod_name = prod.non_terminal + "." + str(term)
                                new_rhses.append([new_prod_name])
                                unchecked_prods.append(Production(new_prod_name, groups[term]))
                        unchecked_prods.append(Production(prod.non_terminal, new_rhses))
                        grammar_changed = True
        self.make_prods(new_prods)

    def remove_left_recursion(self):
        non_terminals = list(self.prods.keys())
        for i, non_terminal in enumerate(non_terminals):
            grammar_changed = True
            while grammar_changed:
                grammar_changed = False
                rhs_i = self.prods[non_terminal].rhses
                for rhs in rhs_i:
                    for A_j in non_terminals[:i]:
                        if rhs[0] == A_j:
                            rhs_revised = rhs[1:]
                            self.prods[non_terminal].rhses.remove(rhs)
                            grammar_changed = True
                            for prod in self.prods[A_j].rhses:
                                self.prods[non_terminal].rhses.append(prod + rhs_revised)

            alpha_set = [prod[1:] for prod in self.prods[non_terminal].rhses if prod[0] == non_terminal]
            beta_set = [prod for prod in self.prods[non_terminal].rhses if prod[0] != non_terminal]
            if len(alpha_set) > 0:
                self.prods.pop(non_terminal)
                non_terminal_new = non_terminal + '.new'
                self.prods[non_terminal] = Production(non_terminal, [
                    beta_i + [non_terminal_new] if beta_i != epsilon else [non_terminal_new] for beta_i in beta_set])
                self.prods[non_terminal_new] = Production(non_terminal_new,
                                                          [alpha_i + [non_terminal_new] for alpha_i in alpha_set])
                self.prods[non_terminal_new].rhses += [epsilon]

    @staticmethod
    def make_grammar(compressed_prods):
        start = compressed_prods[0][0]
        productions = []
        for c_prod in compressed_prods:
            r = Production(c_prod[0], c_prod[1:])
            productions.append(r)
        return Grammar(productions, start)


class LL1Grammar:
    """
        first sets don't contain epsilon however values which lead to epsilons are kept in epsilons
        EOF does not automatically added to first product in grammar
        first sets keep next rhs in dfa table for each none terminal and token
    """

    def __init__(self, grammar):
        self.grammar = grammar
        self.grammar.remove_left_recursion()
        self.grammar.left_factorize_prods()
        self.clean_grammar()
        self.epsilons = list()
        self.first_sets = dict()
        self.follow_sets = dict()
        self.find_epsilon_non_terminals()
        self.make_first_sets()
        self.make_follow_sets()

    def find_epsilon_non_terminals(self):
        self.epsilons = list()
        for prod in self.grammar.prods.values():
            if epsilon in prod.rhses:
                self.epsilons.append(prod.non_terminal)
        epsilons_changed = True
        while epsilons_changed:
            epsilons_changed = False
            for prod in self.grammar.prods.values():
                if not ((prod.non_terminal in self.epsilons) or any(isinstance(rhs, Token) for rhs in prod.rhses)):
                    for rhs in prod.rhses:
                        if all((isinstance(value, Directive) or value in self.epsilons) for value in rhs):
                            epsilons_changed = True
                            self.epsilons.append(prod.non_terminal)
                            break

    def make_first_sets(self):
        for non_terminal in self.grammar.prods.keys():
            self.first_sets[non_terminal] = dict()
        grammar_changed = True
        while grammar_changed:
            grammar_changed = False
            for prod in self.grammar.prods.values():
                for rhs in prod.rhses:
                    if not (rhs == epsilon):
                        for value in list(filter(lambda x: not isinstance(x, Directive), rhs)):
                            if isinstance(value, Token):
                                if not (value in self.first_sets[prod.non_terminal]):
                                    self.first_sets[prod.non_terminal][value] = rhs
                                    grammar_changed = True
                            else:
                                for token in self.first_sets[value]:
                                    if not (token in self.first_sets[prod.non_terminal]):
                                        self.first_sets[prod.non_terminal][token] = rhs
                                        grammar_changed = True
                            if not value in self.epsilons:
                                break

    def make_follow_sets(self):
        for non_terminal in self.grammar.prods.keys():
            self.follow_sets[non_terminal] = set()
        grammar_changed = True
        while grammar_changed:
            grammar_changed = False
            for prod in self.grammar.prods.values():
                for naive_rhs in prod.rhses:
                    rhs = list(filter(lambda x: not isinstance(x, Directive), naive_rhs))
                    if not (rhs == epsilon):
                        for i in range(len(rhs) - 1):
                            if rhs[i] in self.follow_sets:
                                index = i + 1
                                while True:
                                    if index >= len(rhs):
                                        break
                                    if isinstance(rhs[index], Token):
                                        grammar_changed = not (rhs[index] in self.follow_sets[rhs[i]])
                                        self.follow_sets[rhs[i]].add(rhs[index])
                                        break
                                    elif rhs[index] in self.first_sets:
                                        for token in self.first_sets[rhs[index]]:
                                            if not (token in self.follow_sets[rhs[i]]):
                                                grammar_changed = True
                                                self.follow_sets[rhs[i]].add(token)
                                        if not (rhs[index] in self.epsilons):
                                            break
                                    index += 1
        grammar_changed = True
        while grammar_changed:
            grammar_changed = False
            for none_terminal in self.grammar.prods:
                for naive_rhs in self.grammar.prods[none_terminal].rhses:
                    rhs = list(filter(lambda x: not isinstance(x, Directive), naive_rhs))
                    if rhs[0] != epsilon[0]:
                        follow_chain = [none_terminal] + list(reversed(rhs))
                        for i in range(1, len(follow_chain)):
                            value = follow_chain[i]
                            if isinstance(value, Token):
                                break
                            for token in self.follow_sets[follow_chain[i - 1]]:
                                if not (token in self.follow_sets[value]):
                                    self.follow_sets[value].add(token)
                                    grammar_changed = True
                            if not (value in self.epsilons):
                                break

    def clean_grammar(self):
        grammar_changed = True
        while grammar_changed:
            grammar_changed = False
            for prod in list(self.grammar.prods.values()):
                if (len(prod.rhses) == 1) and (epsilon in prod.rhses):
                    for other_prod in list(self.grammar.prods.values()):
                        for rhs in other_prod.rhses:
                            if prod.non_terminal in rhs:
                                rhs.remove(prod.non_terminal)
                        for i in range(len(other_prod.rhses)):
                            if len(other_prod.rhses[i]) == 0:
                                other_prod.rhses[i] = epsilon
                    grammar_changed = True
                    self.grammar.prods.pop(prod.non_terminal)
