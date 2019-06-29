from LexicalAnalyzer import LexicalAnalyzer
from Token import Token


class TokenHandler:
    def __init__(self, dfa, excluded_tokens):
        self.dfa = dfa
        self.excluded_tokens = excluded_tokens
        self.file_in = None
        self.error_writer = None

    def set_io(self, file_in, error_writer):
        self.file_in = file_in
        self.error_writer = error_writer

    def get_next_token(self):
        model = LexicalAnalyzer(self.file_in, self.dfa)
        token = model.get_next_token()
        line = 1
        try:
            while True:
                lexeme, tok, error = next(token)
                line += lexeme.count("\n")
                self.error_writer.update_line(line)
                if not error:
                    if tok not in self.excluded_tokens:
                        yield Token(token_type=tok, token_value=lexeme)
                else:
                    lexeme = lexeme.lstrip()
                    self.error_writer.write("({}, invalid input)\n".format(lexeme))
        except StopIteration:
            pass
