from CGrammar import cs
from Grammar import Grammar, LL1Grammar
from Parser import Parser
from Production import epsilon
from Token import CTokenType, Token


def test_rules(grammar):
    for prod in grammar.prods:
        print("{} -> {}".format(prod, grammar.prods[prod].rhses))


def test_epsilons(ll1_grammar):
    print("epsilons: {}", ll1_grammar.epsilons)


# rules = [
#     ["E", ["T", "A", Token(CTokenType.EOF)]],
#     ["A", [cs("+"), "T", "A"], epsilon],
#     ["T", ["F", "B"], epsilon],
#     ["B",
#      [cs("*"), "F", "B"],
#      epsilon
#      ],
#     ["F", [cs("("), "E", cs(")")], [Token(CTokenType.ID)]],
    # ["C", epsilon]
    # ["left", [cs("*"), "left_a"], [cs("*"), "left_a", cs("+")]],
    # ["left_a", [cs("+")], epsilon],
    # ["R1", ["R2", cs("+")]],
    # ["R2", ["R1", cs("*")], epsilon]
# ]
#
# grammar = LL1Grammar(Grammar.make_grammar(rules))
# test_rules(grammar.grammar)
#
#
# # test_epsilons(grammar)
# # # grammar.first_sets = {"E": [cs("("), Token(CTokenType.ID)],
# # #                       "A": [cs("+"), epsilon],
# # #                       "T": [cs("("), Token(CTokenType.ID)],
# # #                       "B": [cs("*"), epsilon],
# # #                       "F": [cs("("), Token(CTokenType.ID)]}
# # #
# # # grammar.follow_sets = {"E": [cs(")"), Token(CTokenType.EOF)],
# # #                        "A": [cs(")"), Token(CTokenType.EOF)],
# # #                        "T": [cs(")"), Token(CTokenType.EOF), cs("+")],
# # #                        "B": [cs(")"), Token(CTokenType.EOF), cs("+")],
# # #                        "F": [cs(")"), Token(CTokenType.EOF), cs("+"), cs("*")]}
# #
# parser = Parser(grammar)
# inp = [Token(CTokenType.ID), Token(CTokenType.EOF)]
# tok = inp[0]
# count = 1
# while True:
#     error_state, get_next, error_type = parser.parse(tok)
#     if parser.current_fsm.name == parser.grammar.grammar.start_symbol and \
#             parser.current_fsm.current_state == parser.current_fsm.final:
#         print("Successfully parsed input")
#         break
#     if get_next:
#         tok = inp[count]
#         count += 1

import unittest

class DirectiveSymbolIgnoringTest(unittest.TestCase):
    pass

from DirectiveSymbol import DirectiveSymbol
class DirectiveSymbolTest(DirectiveSymbol):
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return "dir:" + self.s

def test_grammar_left_factoring():


    directive = DirectiveSymbolTest
    compressed_grammar_test = [
        ["A", ["B", directive("1")], ["B", directive("1"), Token("c")], ["B", directive("2"), Token("d")]],
        ["B", [directive("3"), Token("a")], [directive("3"), Token("b")]],
        ["C", ["D", Token("h"), directive("4"),], ["D"]],
        ["D", ["E", directive("5"), Token("t")],
         ["E", Token("t1"), directive("6")],
         ["G", Token("g"), directive("7")],
         ["G", directive("8"), Token("g"), Token("g1")],
         [directive("9")]],
        ["E", [directive("10")]],
        ["G", [Token("h"), directive("11")]]
    ]
    compressed_grammar_check = [
        ["A", ["B", ], ["B", Token("c")], ["B", Token("d")]],
        ["B", [Token("a")], [Token("b")]],
        ["C", ["D", Token("h"), ], ["D"]],
        ["D", ["E", Token("t")],
         ["E", Token("t1"), ],
         ["G", Token("g"), ],
         ["G", Token("g"), Token("g1")],
         epsilon],
        ["E", epsilon],
        ["G", [Token("h"), ]]
    ]
    grammar = Grammar.make_grammar(compressed_grammar_test)
    grammar = LL1Grammar(grammar)
    grammar.print()
    grammar2 = Grammar.make_grammar(compressed_grammar_check)
    grammar2 = LL1Grammar(grammar2)
    grammar2.print()
test_grammar_left_factoring()
