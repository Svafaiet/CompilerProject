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

    def handle_semantic_symbol(self, semantic_symbol, **kwargs):
        current_node = kwargs.pop('current_node', None)
        semantic_symbol_type = semantic_symbol.type
        semantic_routine = None
        if current_node is None and semantic_symbol_type != "scope_end":
            if semantic_symbol_type == 'DECLARE_TYPE':
                self.prev_sym_entry = None
            #Todo handle errors
            return

        if semantic_symbol_type == 'DECLARE_TYPE':
            self.prev_sym_entry = current_node
        semantic_routine = eval("self." + semantic_symbol_type.lower())
        semantic_routine(current_node, **kwargs)

    def scope_start(self, current_node, **kwargs):
        non_terminal = kwargs.pop('current_non_terminal', None)
        self.stack.append((len(self.symbol_table), non_terminal))

    def scope_end(self, *args, **kwargs):
        self.symbol_table = self.symbol_table[:self.stack[-1][0]]
        del self.stack[-1]

    def declare_type(self, current_node, **kwargs):
        entry = SymbolTableRecord(type=current_node.token_value)
        self.symbol_table.append(entry)
        self.symbol_table[-1].attributes['dec-type'] = "variable"

    def declare_name(self, current_node, **kwargs):
        name = current_node.token_value
        if self.prev_sym_entry is not None and name is not None:
            self.symbol_table[-1].name = name

    def declare_var_size(self, current_node, **kwargs):
        if self.prev_sym_entry is not None and current_node is not None:
            self.symbol_table[-1].attributes["var_size"] = current_node.token_value

    def function(self, *args, **kwargs):
        self.symbol_table[-1].attributes['dec-type'] = "function"

    def add_param(self, current_node, **kwargs):
        param = current_node
        ind = -1
        func = self.symbol_table[ind]
        while func.attributes['dec-type'] != "function":
            ind -= 1
            func = self.symbol_table[ind]
        if self.prev_sym_entry is not None and param is not None:
            if 'param-len' in func.attributes:
                if func.attributes["param-len"] == 0:
                    pass
                    #TODO check error
                elif param == ck("void") or (hasattr(param, 'children') and param.chilren[0] == ck("void")):
                    pass
                    #TODO check error
                else:
                    func.attributes["param-len"] += 1
            else:
                if param == ck("int") or (hasattr(param, 'children') and param.chilren[0] == ck("int")):
                    func.attributes["param-len"] = 1
                if param == ck("void") or (hasattr(param, 'children') and param.chilren[0] == ck("void")):
                    func.attributes["param-len"] = 0

    def check_break(self):
        for scope in self.stack[::-1]:
            if scope[1] == "iteration_stmt" or scope[1] == "switch-stmt":
                return True
        return False

    def check_main(self):
        if self.symbol_table[-1].type != ck("void") or self.symbol_table[-1].name != "main" \
                or self.symbol_table[-1].attribures["dec-type"] != "function" \
                or self.symbol_table[-1].attributes["param-len"] != 0:
            return False
        return True
