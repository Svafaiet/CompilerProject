from LexicalAnalyzer import LexicalAnalyzer


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
        # with open('scanner.txt', mode='w') as output_file:
        with open("lexical_errors.txt", mode="a") as err_file:
            line = 1
            last_line = 1
            # print_line = True
            first_error = True
            try:
                while True:
                    lexeme, tok, error = next(token)
                    if '\n' in lexeme:
                        # print_line = True
                        line += lexeme.count("\n")
                    if not error:
                        if tok not in self.excluded_tokens:
                            yield lexeme, tok
                            # if print_line:
                            #     if line > 1:
                            #         output_file.write('\n')
                            #     output_file.write("{}. ".format(line))
                            #     print_line = False
                            # output_file.write("({}, {}) ".format(tok.name, lexeme))
                    else:
                        lexeme = lexeme.lstrip()
                        if last_line == line:
                            err_file.write("({}, invalid input) ".format(lexeme))
                        else:
                            if not first_error:
                                err_file.write("\n")
                            first_error = False
                            err_file.write("{}. ".format(line))
                            err_file.write("({}, invalid input) ".format(lexeme))
                        last_line = line
            except StopIteration:
                pass
