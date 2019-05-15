from enum import Enum


class Token:
    pass


class CTokenType(Enum):
    NUM = "NUM"
    KEYWORD = "KEYWORD"
    ID = "ID"
    SYMBOL = "SYMBOL"
    COMMENT = "COMMENT"
    WHITE_SPACE = "WHITESPACE"
    EOF = "EOF"


class CToken(Token):
    def __init__(self, token_type, token_value=None):
        self.token_type = token_type
        self.token_value = token_value

    def __eq__(self, other):
        return (self.token_type == other.token_type) and \
               (self.token_value == other.token_value if
                (self.token_value is not None) and (other.token_value is not None) else True)
