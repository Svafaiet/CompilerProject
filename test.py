from CompilerProject.Grammar import Grammar
from CompilerProject.CGrammar import compressed_grammar

grammar = Grammar.make_grammar(compressed_grammar)
grammar.remove_left_recursion()