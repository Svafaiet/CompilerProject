from copy import deepcopy
from functools import reduce


class Epsilon:
    def __hash__(self):
        return hash("epsilon")

    def __eq__(self, other):
        return isinstance(other, Epsilon)

    def __str__(self):
        return "__EPSILON__"

epsilon = [Epsilon()]


class Production:
    def __init__(self, non_terminal, rhses):
        self.non_terminal = non_terminal
        self.rhses = rhses

    # def left_factorize(self):
    #     return Production.left_factorize_rhses(rhs_group=self.rhses, prefix=[], production_name=self.non_terminal)
    #
    # @staticmethod
    # def left_factorize_rhses(rhs_group, prefix, production_name):
    #     groups = dict()
    #     for rhs in rhs_group:
    #         if len(rhs) == 0:
    #             groups[epsilon[0]] = []
    #         else:
    #             if not rhs[0] in groups:
    #                 groups[rhs[0]] = []
    #             groups[rhs[0]] += [rhs[1:], ]
    #
    #     if len(groups) > 1:
    #         if len(prefix) > 0:
    #             prefix_name = reduce(lambda str1, str2: str(str1) + str(str2), prefix)
    #             suffix_name = production_name + "." + prefix_name
    #             return [Production(production_name, [[prefix_name, suffix_name], ]),
    #                     Production(suffix_name, list(rhs_group))] + \
    #                    Production.left_factorize_rhses(rhs_group, [], suffix_name)
    #
    #     if len(groups) == len(rhs_group):
    #         if len(prefix) == 0:
    #             return [Production(production_name, list((x if len(x) > 0 else epsilon) for x in list(rhs_group))), ]
    #         else:
    #             prefix_name = reduce(lambda str1, str2: str(str1) + str(str2), prefix)
    #             return [
    #                 Production(production_name + "." + prefix_name, [list(list(x) for x in list(groups.keys())), ]),
    #                 Production(production_name, [list(prefix) + [production_name + "." + prefix_name, ], ])
    #             ]
    #     elif len(groups) == 1:
    #         return Production.left_factorize_rhses(list(groups[rhs_group[0][0]]), prefix + [rhs_group[0][0]],
    #                                                production_name)
    #     else:
    #         new_rhses = []
    #         new_prods = []
    #         for group_key in groups.keys():
    #             if isinstance(group_key, Epsilon):
    #                 new_rhses.append(epsilon)
    #             else:
    #                 suffix_name = production_name + "." + str(group_key)
    #                 new_rhses.append([suffix_name])
    #                 new_prods += Production.left_factorize_rhses(groups[group_key], [group_key], suffix_name)
    #         new_prods.append(Production(production_name, new_rhses))
    #         return new_prods
