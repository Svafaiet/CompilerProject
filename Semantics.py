from CGrammar import ck, cs, s
from Token import Token, CTokenType


class SymbolTableRecord:
    def __init__(self, type, name=None):
        self.type = type
        self.name = name
        self.attributes = dict()


class Semantics:
    def __init__(self, file_error):
        self.file_error = file_error
        self.stack = []
        self.symbol_table = []
        self.prev_sym_entry = None
        self.function_call_stack = []
        self.expression_stack = []
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

    def err(self, error_type, id_tok_val=None):
        with open(file=self.file_error, mode="a") as f:
            error_types = {
                "main":             "main function not found!",
                "scoping":          "{} is not defined.".format(id_tok_val),
                "variable_void":    "Illegal type of void.",
                "arg_count":        "Mismatch in number of arguments of {}.".format(id_tok_val),
                "continue":         "No 'while' found for 'continue'.",
                "break":            "No 'while' or 'switch' found for 'break'.",
                "operand_mismatch": "type mismatch in operands",
            }
            f.write(error_types.get(error_type))

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
                if current_node.token_value != '[':
                    self.symbol_table[-1].attributes["var-size"] = current_node.token_value
                else:
                    self.symbol_table[-1].attributes["var-size"] = '0'

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

    def check_break(self, *args, **kwargs):
        for scope in self.stack[::-1]:
            if scope[1] == "iteration-stmt" or scope[1] == "switch-stmt":
                return True
        ##Todo handle error
        return False

    def check_continue(self, *args, **kwargs):
        for scope in self.stack[::-1]:
            if scope[1] == "iteration_stmt":
                return True
        ##Todo handle error
        return False

    def check_scope(self, current_node, **kwargs):
        name = current_node.token_value
        if self.get_sym_table_entry(name) is not None:
            return True
        else:
            #todo handle errors
            return False

    def check_main(self):
        if self.symbol_table[-1].type != ck("void") or self.symbol_table[-1].name != "main" \
                or self.symbol_table[-1].attribures["dec-type"] != "function" \
                or self.symbol_table[-1].attributes["param-len"] != 0:
            return False
        return True

    def check_func_args_begin(self, current_node, **kwargs):
        func_name = current_node.token_value
        for entry in self.symbol_table[::-1]:
            if entry.name == func_name and entry.attributes['dec-type'] == "function":
                self.function_call_stack.append([entry, 0])
                break

    def check_func_args_end(self, *args, **kwargs):
        if self.function_call_stack[-1][0].attributes['param-len'] != self.function_call_stack[-1][1]:
            ##todo handle errors
            self.function_call_stack.pop()
            pass
        else:
            self.function_call_stack.pop()

    def arg(self, *args, **kwargs):
        self.function_call_stack[-1][1] += 1

    def check_var_type(self, *args, **kwargs):
        if self.symbol_table[-1].attributes['dec-type'] == "variable" and self.symbol_table[-1].type == "void":
            self.symbol_table.pop()
            #todo handle errors
            pass

    def get_sym_table_entry(self, name):
        for entry in self.symbol_table[::-1]:
            if entry.name == name:
                return entry
        else:
            return None

    def begin_expression_check(self, *args, **kwargs):
        self.expression_stack.append([])

    def end_expression_check(self, *args, **kwargs):
        expr = self.expression_stack[-1]
        for ent in expr:
            item = ent[0]
            if item == Token(CTokenType.ID):
                item = self.get_sym_table_entry(item.token_value)
                if item.attributes['dec-type'] == 'function' and item.type == 'void' and len(expr) > 1:
                    #todo handle errors
                    self.expression_stack.pop()
                    return
                if 'var-size' in item.attributes and ent[1] is None:
                    #todo handle errors
                    self.expression_stack.pop()
                    return

        else:
            self.expression_stack.pop()
            return False

    def add_var_to_expression(self, current_node, **kwargs):
        self.expression_stack[-1].append([current_node, None])

    def check_array(self, current_node, **kwargs):
        entry = self.get_sym_table_entry(current_node.token_value)
        if 'var-size' not in entry.attributes:
            #todo handle erros
            pass
        else:
            self.expression_stack[-1][-1][1] = 'array'
            return False

    def check_expression_func(self, current_node, **kwargs):
        entry = self.get_sym_table_entry(current_node.token_value)
        if entry.attributes['dec-type'] == 'function' and entry.type == 'void':
            if len(self.expression_stack) > 1:
                #todo handle errors
                pass
            elif len(self.expression_stack[-1]) > 1:
                #todo handle errors
                pass
            else:
                return False

    def end_secondary_expression_check(self, *args, **kwargs):
        expr = self.expression_stack[-1]
        for ent in expr:
            item = ent[0]
            if item == Token(CTokenType.ID):
                item = self.get_sym_table_entry(item.token_value)
                if item.attributes['dec-type'] == 'function' and item.type == 'void':
                    #todo handle errors
                    self.expression_stack.pop()
                    return
                if 'var-size' in item.attributes and ent[1] is None:
                    #todo handle errors
                    self.expression_stack.pop()
                    return

        else:
            self.expression_stack.pop()
            return False
