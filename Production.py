from copy import deepcopy
from functools import reduce


class Epsilon:
    pass


epsilon = [Epsilon()]


class Production:
    def __init__(self, non_terminal, rhses):
        self.non_terminal = non_terminal
        self.rhses = rhses

    def left_factorize(self):
        left_factorized_prod = Production.left_factorize_rhses(rhs_group=self.rhses, prefix=[])
        return [Production(self.non_terminal, left_factorized_prod[0]), ] + left_factorized_prod[1]

    @staticmethod
    def left_factorize_rhses(rhs_group, prefix): # fixme epsilons not handled
        groups = dict()
        epsilon_flag = False
        for rhs in rhs_group:
            if len(rhs) == 0:
                epsilon_flag = True
            else:
                if not rhs[0] in groups:
                    groups[rhs[0]] = []
                groups[rhs[0]] += [rhs[1:], ]

        if len(groups) == len(rhs_group):
            return deepcopy(rhs_group), []
        elif epsilon_flag or len(groups) > 1:
            new_prods = []
            left_factorized_rhses = []
            new_prod_name = reduce(lambda str1, str2: str1 + str2, prefix)
            new_prods += [Production(new_prod_name, deepcopy(prefix)), ]
            for group_key in groups.keys():
                group_factorization = Production.left_factorize_rhses(groups[group_key],
                                                                      deepcopy(prefix) + [group_key, ])
                for left_factorized_rhs in group_factorization[0]:
                    left_factorized_rhses += [[new_prod_name, ] + left_factorized_rhs, ]
                new_prods += group_factorization[1]
            return left_factorized_rhses, new_prods
        elif len(groups) == 1:
            return Production.left_factorize_rhses(rhs_group, prefix + rhs_group[0][0])
