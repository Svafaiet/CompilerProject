from CompilerProject.Parser import Parser
from CompilerProject.Production import epsilon
from CompilerProject.Token import CTokenType, Token
from CompilerProject.CGrammar import cs, ck
from CompilerProject.Grammar import Grammar, LL1Grammar

rules = [
    ["E", ["T", "A"]],
    ["A", [cs("+"), "T", "A"], epsilon],
    ["T", ["F", "B"]],
    ["B",
     [cs("*"), "F", "B"],
     epsilon
     ],
    ["F", [cs("("), "E", cs(")")], [Token(CTokenType.ID)]]
]

grammar = LL1Grammar(Grammar.make_grammar(rules))
grammar.first_sets = {"E": [cs("("), Token(CTokenType.ID)],
                      "A": [cs("+"), epsilon],
                      "T": [cs("("), Token(CTokenType.ID)],
                      "B": [cs("*"), epsilon],
                      "F": [cs("("), Token(CTokenType.ID)]}

grammar.follow_sets = {"E": [cs(")"), Token(CTokenType.EOF)],
                       "A": [cs(")"), Token(CTokenType.EOF)],
                       "T": [cs(")"), Token(CTokenType.EOF), cs("+")],
                       "B": [cs(")"), Token(CTokenType.EOF), cs("+")],
                       "F": [cs(")"), Token(CTokenType.EOF), cs("+"), cs("*")]}

parser = Parser(grammar)
inp = [cs("("), Token(CTokenType.ID), cs(")"), Token(CTokenType.EOF)]
tok = inp[0]
count = 1
while True:
    _, get_next = parser.parse(tok)
    if get_next:
        tok = inp[count]
        count += 1
    if parser.current_fsm.name == parser.grammar.grammar.start_symbol and \
            parser.current_fsm.current_state == parser.current_fsm.final and\
            tok == Token(CTokenType.EOF):
        print("Successfully parsed input")
        break
