from Token import CTokenType


class ParserHandler:
    def __init__(self, parser):
        self.parser = parser
        self.file_error = None

    def set_files(self, file_error):
        self.file_error = file_error

    def parse_token(self, token, line):
        """

        :param token:
        :param line:
        :return: a boolean, the terminate state
        """
        while True:
            if token.token_type == CTokenType.ID or token.token_type == CTokenType.EOF \
                    or token.token_type == CTokenType.NUM:
                token.token_value = None
            error, next_token_needed, error_type = self.parser.parse(token)
            if error:
                err_type, tok = error_type
                self.handle_errors(err_type, line, tok)
                if err_type == 3 or err_type == 4:
                    return True

            if self.parser.current_fsm.name == self.parser.grammar.grammar.start_symbol and \
                    self.parser.current_fsm.current_state == self.parser.current_fsm.final:
                print("Successfully parsed input file")
                return True

            if next_token_needed:
                return False

    def handle_errors(self, error_type, line, token):
        with open(file=self.file_error, mode="a") as f:
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