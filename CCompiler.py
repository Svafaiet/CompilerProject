import CLexicalDFA
from Token import CTokenType, Token
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
        tok_gen = self.token_handler.get_next_token()
        token, line = next(tok_gen)
        while True:
            error, next_token_needed, error_type = parser.parse(token)
            if error:
                err_type, tok = error_type
                self.handle_errors(err_type, line, tok)
                if err_type == 3 or err_type == 4:
                    return
            if next_token_needed:
                token, line = next(tok_gen)

            if self.parser.current_fsm.name == parser.grammar.grammar.start_symbol and \
                    parser.current_fsm.current_state == parser.current_fsm.final:
                print("Successfully parsed input file")
                return

    def handle_errors(self, error_type, line, token):
        with open(file=self.token_handler.file_error, mode="a") as f:
            if error_type == 0:
                f.write("{}: Syntax Error! Missing {}\n".format(line, token.token_type))
            elif error_type == 1:
                f.write("{}: Syntax Error! Unexpected {}\n".format(line, token.token_type))
            elif error_type == 2:
                f.write("{}: Syntax Error! Missing {}\n".format(line, token))
            elif error_type == 3:
                f.write("{}: Syntax Error! Unexpected EndOfFile\n".format(line))
            elif error_type == 4:
                f.write("{}: Syntax Error! Malformed Input\n".format(line))


DEFAULT_FILE_IN_NAME = "scanner.txt"
DEFAULT_FILE_OUT_NAME = "output.txt"
DEFAULT_FILE_ERROR_NAME = "error.txt"

c_lexical_dfa = CLexicalDFA.make_c_lexical_dfa()
not_printing_tokens = [CTokenType.WHITE_SPACE, CTokenType.COMMENT]
c_token_handler = TokenHandler(c_lexical_dfa, not_printing_tokens)
grammar = LL1Grammar(Grammar.make_grammar(compressed_grammar))
parser = Parser(grammar)