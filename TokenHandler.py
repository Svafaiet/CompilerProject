from LexicalAnalyzer import LexicalAnalyzer
from Token import Token


class TokenHandler:
    def __init__(self, dfa, excluded_tokens):
        self.dfa = dfa
        self.excluded_tokens = excluded_tokens
        self.file_in = None
        self.file_error = None

    def set_files(self, file_in, file_error):
        self.file_in = file_in
        self.file_error = file_error

    def get_next_token(self):
        model = LexicalAnalyzer(self.file_in, self.dfa)
        token = model.get_next_token()
        with open(self.file_error, mode="a") as err_file:
            line = 1
            try:
                while True:
                    lexeme, tok, error = next(token)
                    line += lexeme.count("\n")
                    if not error:
                        if tok not in self.excluded_tokens:
                            yield Token(token_type=tok, token_value=lexeme), line
                    else:
                        lexeme = lexeme.lstrip()
                        err_file.write("{}. ({}, invalid input)\n".format(line, lexeme))
            except StopIteration:
                pass
