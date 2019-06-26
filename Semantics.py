

class SymbolTableRecord:
    def __init__(self, type, name=None):
        self.type = type
        self.name = name
        self.attributes = dict()


class Semantics:
    def __init__(self):
        self.stack = []
        self.symbol_table = []
        self.prev_sym_entry = None
    #TODO MAKE OUTPUT

    #TODO CHECK MAIN

    def handle_semantic_symbol(self, **kwargs):
        semantic_symbol = kwargs.get('semantic_symbol', default="SCOPE_START")
        semantic_symbol_type = semantic_symbol.type
        semantic_routine = eval(semantic_symbol_type.lower())
        semantic_routine(kwargs)

    def scope_start(self, **kwargs):
        self.stack.append(len(self.symbol_table))

    def scope_end(self, **kwargs):
        self.symbol_table = self.symbol_table[:self.stack[-1]]
        del self.stack[-1]

    def declare_type(self, **kwargs):
        current_node = kwargs.get('current_node', None)
        if current_node is None:
            self.prev_sym_entry = None
        type = current_node.children[0]
        entry = SymbolTableRecord(type=type)
        self.symbol_table.append(entry)
        self.prev_sym_entry = entry

    def declare_name(self, **kwargs):
        name = kwargs.get('current_node', None)
        if self.prev_sym_entry is not None and name is not None:
            self.symbol_table[-1].name = name

    def declare_var_size(self, **kwargs):
        var_size = kwargs.get('current_node', None)
        if self.prev_sym_entry is not None and var_size is not None:
            self.symbol_table[-1].attributes["var_size"] = var_size
            self.symbol_table[-1].attributes['dec-type'] = "variable"

    def add_param(self, **kwargs):
        param = kwargs.get('current_node', None)
        if self.prev_sym_entry is not None and param is not None:
            if 'param-len' in self.symbol_table[-1].attributes:
                self.symbol_table[-1].attributes += 1
            else:
                self.symbol_table[-1].attributes = 1
                self.symbol_table[-1].attributes['dec-type'] = "function"

