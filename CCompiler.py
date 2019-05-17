import CLexicalDFA
from TokenHandler import TokenHandler
from Token import CTokenType
from Parser import Parser
from CGrammar import compressed_grammar
from Grammar import LL1Grammar, Grammar


class Compiler:
    def __init__(self, token_handler, parser):
        self.token_handler = token_handler
        self.parser = parser

    def compile(self, file_in, file_out, file_error):
        self.token_handler.set_files(file_in=file_in, file_error=file_error)
        pass


DEFAULT_FILE_IN_NAME = "scanner.txt"
DEFAULT_FILE_OUT_NAME = "output.txt"
DEFAULT_FILE_ERROR_NAME = "error.txt"

c_lexical_dfa = CLexicalDFA.make_c_lexical_dfa()
not_printing_tokens = [CTokenType.WHITE_SPACE, CTokenType.COMMENT]
c_token_handler = TokenHandler(c_lexical_dfa, not_printing_tokens)
grammar = LL1Grammar(Grammar.make_grammar(compressed_grammar))
parser = Parser(grammar)