class LexicalAnalyzer:
    def __init__(self, file, dfa):
        self.file = file
        self.dfa = dfa

    def get_next_token(self):
        with open(self.file, mode='r') as input_file:
            state = self.dfa.init_state
            byte = input_file.read(1)
            lexeme = ""
            while byte:
                lexeme += byte
                state = state.get_next_state(byte)
                if state.goal_type is not None:
                    yield (lexeme, state.goal_type)
                    state = self.dfa.init_state
                    lexeme = ""
                byte = input_file.read(1)

