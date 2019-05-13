from copy import deepcopy
from functools import reduce

class Production:
    def __init__(self, none_terminal, sub_prods):
        self.none_terminal = none_terminal
        self.sub_prods = sub_prods

    def left_factorize(self):
        left_factorized_prod = Production.left_factorize_sub_prods(sub_prod_group=self.sub_prods, prefix=[])
        return [Production(self.none_terminal, left_factorized_prod[0]), ] + left_factorized_prod[1]

    # (left_factorized_sub_prods, new_prods)
    @staticmethod
    def left_factorize_sub_prods(sub_prod_group, prefix):
        groups = dict()
        ebsilon_flag = False
        for sub_prod in sub_prod_group:
            if len(sub_prod) == 0:
                ebsilon_flag = True
            else:
                if not sub_prod[0] in groups:
                    groups[sub_prod[0]] = []
                groups[sub_prod[0]] += [sub_prod[1:], ]

        if len(groups) == len(sub_prod_group):
            return deepcopy(sub_prod_group), []
        elif ebsilon_flag or len(groups) > 1:
            new_prods = []
            left_factorized_sub_prods = []
            new_prod_name = reduce(lambda str1, str2: str1 + str2, prefix)
            new_prods += [Production(new_prod_name, deepcopy(prefix)), ]
            for group_key in groups.keys():
                group_factorization = Production.left_factorize_sub_prods(groups[group_key], deepcopy(prefix) + [group_key, ])
                for left_factorized_sub_prod in group_factorization[0]:
                    left_factorized_sub_prods += [[new_prod_name, ] + left_factorized_sub_prod, ]
                new_prods += group_factorization[1]
            return left_factorized_sub_prods, new_prods
        elif len(groups) == 1:
            return Production.left_factorize_sub_prods(sub_prod_group, prefix + sub_prod_group[0][0])
