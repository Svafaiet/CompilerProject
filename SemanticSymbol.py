from DirectiveSymbol import DirectiveSymbol


class SemanticSymbol(DirectiveSymbol):
    """
    directive for semantic structure
    semantic_handler will generate tables according to param type
    different kinds of type are:
        SCOPE_START
        SCOPE_END


    """
    def __init__(self, t):
        self.type = t

