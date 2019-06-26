import CLexicalDFA
from CodeGenerator import CodeGenerator
from DirectiveHandler import DirectiveHandler
from ParseHandler import ParserHandler
from ParseTree import ParseTree
from Semantics import Semantics
from Token import CTokenType, Token
from TokenHandler import TokenHandler
from Token import CTokenType
from Parser import Parser
from CGrammar import compressed_grammar
from Grammar import LL1Grammar, Grammar


class Compiler:
    def __init__(self, token_handler, parse_handler):
        self.token_handler = token_handler
        self.parse_handler = parse_handler

    def compile(self, file_in, file_out, file_error):
        Compiler.empty_files(file_out, file_error)
        self.token_handler.set_files(file_in=file_in, file_error=file_error)
        self.parse_handler.set_files(file_error=file_error)
        parse_tree = self.parse_handler.parser.parse_tree
        semantics = Semantics()
        code_generator = CodeGenerator()
        directive_handler = DirectiveHandler(semantics, code_generator)
        parse_tree.set_handler(directive_handler)
        tok_gen = self.token_handler.get_next_token()
        is_terminated, error = False, False
        while not is_terminated:
            tok, line = next(tok_gen)
            is_terminated, error = self.parse_handler.parse_token(tok, line)

        view = parser.parse_tree.view()
        with open(file=file_out, mode="w") as f:
            f.write(grammar.grammar.start_symbol + "\n")
            f.write(view)

    @staticmethod
    def empty_files(file_out, file_error):
        with(open(file=file_out, mode="w")):
            pass
        with(open(file=file_error, mode="w")):
            pass


DEFAULT_FILE_IN_NAME = "scanner.txt"
DEFAULT_FILE_OUT_NAME = "output.txt"
DEFAULT_FILE_ERROR_NAME = "error.txt"

c_lexical_dfa = CLexicalDFA.make_c_lexical_dfa()
not_printing_tokens = [CTokenType.WHITE_SPACE, CTokenType.COMMENT]
c_token_handler = TokenHandler(c_lexical_dfa, not_printing_tokens)
grammar = LL1Grammar(Grammar.make_grammar(compressed_grammar))
# for prod in grammar.grammar.prods:
#     print("{}->{}".format(grammar.grammar.prods[prod].non_terminal, grammar.grammar.prods[prod].rhses))
#
# for f in grammar.follow_sets["signed-factor-left"]:
#     print(str(f))]
print(grammar.grammar.compress())
parser = Parser(grammar)
parse_handler = ParserHandler(parser)
compiler = Compiler(c_token_handler, parse_handler)
compiler.compile(DEFAULT_FILE_IN_NAME, DEFAULT_FILE_OUT_NAME, DEFAULT_FILE_ERROR_NAME)