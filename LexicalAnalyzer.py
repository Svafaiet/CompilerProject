class LexicalAnalyzer:
    def __init__(self, file, dfa):
        self.file = file
        self.dfa = dfa

    def get_next_token(self):
        with open(self.file, mode='r') as input_file:
            state = self.dfa.init_state
            byte = input_file.read(1)
            lexeme = ""
            error_detection = False
            while byte:
                lexeme += byte
                last_state = state
                state = state.get_next_state(byte)
                if state is None:
                    error_detection = False
                    if last_state is None or last_state.goal_type is None:
                        error_detection = True
                    else:
                        if self.dfa.init_state.get_next_state(byte) is not None:
                            yield (lexeme[:-1], last_state.goal_type, False)
                        else:
                            error_detection = True
                    if error_detection:
                        yield (lexeme, last_state.goal_type, True)
                        state = self.dfa.init_state
                        last_state = None
                        lexeme = ""
                    else:
                        state = self.dfa.init_state
                        last_state = None
                        lexeme = ""
                        continue
                byte = input_file.read(1)
