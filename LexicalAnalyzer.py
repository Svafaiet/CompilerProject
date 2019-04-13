class LexicalAnalyzer:
    def __init__(self, file, dfa):
        self.file = file
        self.dfa = dfa

    def get_next_token(self):
        with open(self.file, mode='r') as input_file:
            state = self.dfa.init_state
            byte = input_file.read(1)
            lexeme = ""
            while True:
                lexeme += byte
                last_state = state
                state = state.get_next_state(byte)
                if state is None:
                    error_detection = False
                    if last_state is None or last_state.goal_type is None:
                        error_detection = True
                        pass
                    else:
                        if not (self.dfa.init_state.get_next_state(byte) is None):
                            yield (lexeme[:-1], last_state.goal_type)
                        else:
                            error_detection = True
                            pass
                    state = self.dfa.init_state
                    last_state = None
                    lexeme = ""
                    if error_detection:
                        pass
                        # todo handle_errors
                    else:
                        continue
                if not byte:
                    break
                byte = input_file.read(1)
