from Parser import Parser
from Production import epsilon
from Token import CTokenType, Token
from CGrammar import cs, ck
from Grammar import Grammar, LL1Grammar

def test_rules(grammar):
    for prod in grammar.prods:
        print("{} -> {}".format(prod, grammar.prods[prod].rhses))

def test_epsilons(ll1_grammar):
    print("epsilons: {}", ll1_grammar.epsilons)

rules = [
    ["E", ["T", "A", "C", Token(CTokenType.EOF)]],
    ["A", [cs("+"), "T", "A"], epsilon],
    ["T", ["F", "B"]],
    ["B",
     [cs("*"), "F", "B"],
     epsilon
     ],
    ["F", [cs("("), "E", cs(")")], [Token(CTokenType.ID)]],
    ["C", epsilon]
    # ["left", [cs("*"), "left_a"], [cs("*"), "left_a", cs("+")]],
    # ["left_a", [cs("+")], epsilon],
    # ["R1", ["R2", cs("+")]],
    # ["R2", ["R1", cs("*")], epsilon]
]


grammar = LL1Grammar(Grammar.make_grammar(rules))
# test_rules(grammar.grammar)



# test_epsilons(grammar)
# # grammar.first_sets = {"E": [cs("("), Token(CTokenType.ID)],
# #                       "A": [cs("+"), epsilon],
# #                       "T": [cs("("), Token(CTokenType.ID)],
# #                       "B": [cs("*"), epsilon],
# #                       "F": [cs("("), Token(CTokenType.ID)]}
# #
# # grammar.follow_sets = {"E": [cs(")"), Token(CTokenType.EOF)],
# #                        "A": [cs(")"), Token(CTokenType.EOF)],
# #                        "T": [cs(")"), Token(CTokenType.EOF), cs("+")],
# #                        "B": [cs(")"), Token(CTokenType.EOF), cs("+")],
# #                        "F": [cs(")"), Token(CTokenType.EOF), cs("+"), cs("*")]}
#
parser = Parser(grammar)
inp = [Token(CTokenType.ID), Token(CTokenType.EOF)]
tok = inp[0]
count = 1
while True:
    error_state, get_next, error_type = parser.parse(tok)
    if parser.current_fsm.name == parser.grammar.grammar.start_symbol and \
            parser.current_fsm.current_state == parser.current_fsm.final:
        print("Successfully parsed input")
        break
    if get_next:
        tok = inp[count]
        count += 1
