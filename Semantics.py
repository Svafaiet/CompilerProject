from CGrammar import ck, cs, s

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
        current_node = kwargs.get('current_node', None)
        if current_node is not None:
            self.stack.append((len(self.symbol_table), current_node.non_terminal))

    def scope_end(self, **kwargs):
        self.symbol_table = self.symbol_table[:self.stack[-1]]
        del self.stack[-1]

    def declare_type(self, **kwargs):
        current_node = kwargs.get('current_node', None)
        if current_node is None:
            self.prev_sym_entry = None
            return
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
                if self.symbol_table[-1].attributes["param-len"] == 0:
                    pass
                    #TODO check error
                elif param == ck("void") or (hasattr(param, 'children') and param.chilren[0] == ck("void")):
                    pass
                    #TODO check error
                else:
                    self.symbol_table[-1].attributes["param-len"] += 1
            else:
                if param == ck("int") or (hasattr(param, 'children') and param.chilren[0] == ck("int")):
                    self.symbol_table[-1].attributes["param-len"] = 1
                if param == ck("void") or (hasattr(param, 'children') and param.chilren[0] == ck("void")):
                    self.symbol_table[-1].attributes["param-len"] = 0
                self.symbol_table[-1].attributes['dec-type'] = "function"

    def check_break(self):
        for scope in self.stack[::-1]:
            if scope[1] == "iteration_stmt" or scope[1] == "switch-stmt":
                return True
        return False

    def check_main(self):
        if self.symbol_table[-1].type != ck("void") or self.symbol_table[-1].name != "main" \
                or "dec-type" not in self.symbol_table[-1].attributes \
                or self.symbol_table[-1].attribures["dec-type"] != "function" \
                or self.symbol_table[-1].attributes["param-len"] != 0:
            return False
        return True
