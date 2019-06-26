

class SymbolTableRecord:
    def __init__(self, name, type, param_len):
        self.name = name
        self.type = type
        self.param_len = 0


class Semantics:
    def __init__(self):
        self.stack = []
        self.symbol_table = []
    #TODO MAKE OUTPUT

    #TODO CHECK MAIN

    def handle_semantic_symbol(self, **kwargs):
        semantic_symbol = kwargs.get('semantic_symbol', default="SCOPE_START")
        semantic_symbol_type = semantic_symbol.type
        semantic_routine = eval(semantic_symbol_type.lower())
        semantic_routine(kwargs)

    def scope_start(self, **kwargs):
        prev_nonterminal = kwargs.get('previous_nonterminal', None)
        prev_node = kwargs.get('current_node', None)
        self.stack.append(len(self.symbol_table))

    def scope_end(self, **kwargs):
        self.symbol_table = self.symbol_table[:self.stack[-1]]
        del self.stack[-1]

