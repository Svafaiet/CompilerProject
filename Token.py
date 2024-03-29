from enum import Enum


class CTokenType(Enum):
    NUM = "NUM"
    KEYWORD = "KEYWORD"
    ID = "ID"
    SYMBOL = "SYMBOL"
    COMMENT = "COMMENT"
    WHITE_SPACE = "WHITESPACE"

# class TokenType(Enum):
    EOF = "EOF"


class Token:
    def __init__(self, token_type, token_value=None):
        self.token_type = token_type
        self.token_value = token_value

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (self.token_type == other.token_type) and \
               (True if (self.token_value is None) or (other.token_value is None)
                else self.token_value == other.token_value)

    def __hash__(self):
        if self.token_type in [CTokenType.ID, CTokenType.NUM, CTokenType.EOF]:
            return hash(self.token_type)
        else:
            return hash(self.token_value)

    def __str__(self):
        if self.token_value:
            return self.token_value
        else:
            return str(self.token_type)