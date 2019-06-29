from Token import CTokenType


class ParserHandler:
    def __init__(self, parser):
        self.parser = parser
        self.error_writer = None

    def set_io(self, error_writer):
        self.error_writer = error_writer

    def parse_token(self, token):
        """

        :param token:
        :param line:
        :return: a boolean, the terminate state
        """
        while True:
            error, next_token_needed, error_type = self.parser.parse(token)
            if error:
                err_type, tok = error_type
                self.handle_errors(err_type, tok)
                if err_type == 3 or err_type == 4:
                    return True, True

            if self.parser.current_fsm.name == self.parser.grammar.grammar.start_symbol and \
                    self.parser.current_fsm.current_state == self.parser.current_fsm.final:
                print("Successfully parsed input file")
                return True, error

            if next_token_needed:
                return False, error

    def handle_errors(self, error_type, token):
        if error_type == 0:
            self.error_writer.write("Syntax Error! Missing {}\n".format(token.token_type))
        elif error_type == 1:
            self.error_writer.write("Syntax Error! Unexpected {}\n".format(token.token_type))
        elif error_type == 2:
            self.error_writer.write("Syntax Error! Missing {}\n".format(token))
        elif error_type == 3:
            self.error_writer.write("Syntax Error! Unexpected EndOfFile\n")
        elif error_type == 4:
            self.error_writer.write("Syntax Error! Malformed Input\n")
