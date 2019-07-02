from CGrammar import ck, cs, s
from Token import Token, CTokenType


class SymbolTableRecord:
    def __init__(self, type, name=None):
        self.type = type
        self.name = name
        self.attributes = dict()


class Semantics:
    def __init__(self, error_writer):
        self.stack = []
        self.symbol_table = []
        self.prev_sym_entry = None
        self.function_call_stack = []
        self.error_writer = error_writer
        self.expression_stack = []
        self.function_stack = []

        self.symbol_table.append(SymbolTableRecord("void", "__global__"))
        self.symbol_table[-1].attributes = {"dec-type": "function"}
        self.stack.append([0, "__global__"])

    def get_sym_table_funcless_entry(self, name):
        func_less_list = list(filter(lambda x: (x.attributes['dec-type'] != "function"), self.symbol_table[::-1]))
        for i, entry in enumerate(func_less_list):
            if entry.name == name:
                return entry, len(func_less_list) - i - 1
        else:
            return None, None

    def get_sym_table_entry(self, name):
        for i, entry in enumerate(self.symbol_table[::-1]):
            if entry.name == name:
                return entry, len(self.symbol_table) - i - 1
        else:
            return None, None

    def set_ar(self, ar):
        for entry in self.symbol_table[::-1]:
            if entry.attributes['dec-type'] == 'function' and entry.name == ar.func_name:
                entry.attributes['ar'] = ar

    def err(self, error_type, id_tok_val=None):
        error_types = {
            "main": "Main function not found or is invalid!\n",
            "scoping": "{} is not defined.\n".format(id_tok_val),
            "variable_void": "Illegal type of void for variable {}.\n".format(id_tok_val),
            "arg_count": "Mismatch in number of arguments of {}.\n".format(id_tok_val),
            "continue": "No 'while' found for 'continue'.\n",
            "break": "No 'while' or 'switch' found for 'break'.\n",
            "operand_mismatch": "Type mismatch in operands\n",
            "invalid_parameters": "Invalid parameter of type void for function {}. function already has a parameter\n".format(
                id_tok_val),
            "invalid_variable_indexing": "Variable {} is not an array and can not be indexed\n".format(id_tok_val),
            "invalid_index": "Invalid index for array {}\n".format(id_tok_val),
            "second_declaration": "This is a second declaration of {}\n".format(id_tok_val),
            "int_function_no_ret_val": "Function {} returns nothing\n".format(id_tok_val),
            "void_function_ret_val": "Function {} is of type void but is returning value\n".format(id_tok_val),
            "return": "No function found for return\n",
            "non-function": "{} is not a function\n".format(id_tok_val),
        }
        self.error_writer.write(error_types.get(error_type))

    def handle_semantic_symbol(self, semantic_symbol, **kwargs):
        current_node = kwargs.pop('current_node', None)
        semantic_symbol_type = semantic_symbol.type
        semantic_routine = None
        if current_node is None and semantic_symbol_type != "scope_end":
            if semantic_symbol_type == 'DECLARE_TYPE':
                self.prev_sym_entry = None
            # Todo handle errors
            return

        if semantic_symbol_type == 'DECLARE_TYPE':
            self.prev_sym_entry = current_node
        semantic_routine = eval("self." + semantic_symbol_type.lower())
        # semantic_routine(current_node, **kwargs)
        try:
            semantic_routine(current_node, **kwargs)
        except Exception as e:
            print(e)

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
            if self.get_sym_table_entry(name) == (None, None):
                self.symbol_table[-1].name = name
            else:
                self.err("second_declaration", name)
                self.symbol_table.pop()

    def declare_var_size(self, current_node, **kwargs):
        if self.prev_sym_entry is not None and current_node is not None:
            if current_node.token_value != '[':
                self.symbol_table[-1].attributes["var-size"] = current_node.token_value
            else:
                self.symbol_table[-1].attributes["var-size"] = '0'

    def function(self, *args, **kwargs):
        self.symbol_table[-1].attributes['dec-type'] = "function"
        self.function_stack.append(self.symbol_table[-1])

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
                    self.err('invalid_parameters', func.name)
                    self.symbol_table.pop(ind)
                elif param == ck("void") or (hasattr(param, 'children') and param.chilren[0] == ck("void")):
                    self.err('invalid_parameters', func.name)
                    self.symbol_table.pop(ind)
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
                break
        else:
            self.err("break")

    def check_continue(self, *args, **kwargs):
        for scope in self.stack[::-1]:
            if scope[1] == "iteration_stmt":
                break
        else:
            self.err("continue")

    def check_scope(self, current_node, **kwargs):
        name = current_node.token_value
        if self.get_sym_table_entry(name) == (None, None):
            self.err("scoping", name)

    def check_main(self, *args, **kwargs):
        if self.symbol_table[-1].type != "void" or self.symbol_table[-1].name != "main" \
                or self.symbol_table[-1].attributes["dec-type"] != "function" \
                or self.symbol_table[-1].attributes["param-len"] != 0:
            self.err("main")

    def check_func_args_begin(self, current_node, **kwargs):
        func_name = current_node.token_value
        for entry in self.symbol_table[::-1]:
            if entry.name == func_name and entry.attributes['dec-type'] == "function":
                self.function_call_stack.append([entry, 0])
                break

    def check_func_args_end(self, *args, **kwargs):
        if self.function_call_stack[-1][0].attributes['param-len'] != self.function_call_stack[-1][1]:
            self.err("arg_count", self.function_call_stack[-1][0].name)
            self.function_call_stack.pop()
        else:
            self.function_call_stack.pop()

    def arg(self, *args, **kwargs):
        self.function_call_stack[-1][1] += 1

    def check_var_type(self, *args, **kwargs):
        if self.symbol_table[-1].attributes['dec-type'] == "variable" and self.symbol_table[-1].type == "void":
            self.err("variable_void", self.symbol_table[-1].name)
            self.symbol_table.pop()

    def begin_expression_check(self, *args, **kwargs):
        self.expression_stack.append([])

    def end_expression_check(self, *args, **kwargs):
        expr = self.expression_stack[-1]
        for ent in expr:
            item = ent[0]
            if item == Token(CTokenType.ID):
                item, _ = self.get_sym_table_entry(item.token_value)
                if item is not None:
                    if item.attributes['dec-type'] == 'function' and item.type == 'void' and len(expr) > 1:
                        self.err("operand_mismatch")
                    if 'var-size' in item.attributes and ent[1] is None:
                        self.err("operand_mismatch")

        self.expression_stack.pop()

    def add_var_to_expression(self, current_node, **kwargs):
        self.expression_stack[-1].append([current_node, None])

    def check_array(self, current_node, **kwargs):
        entry, _ = self.get_sym_table_entry(current_node.token_value)
        if entry is not None:
            if 'var-size' not in entry.attributes:
                self.err("invalid_variable_indexing", entry.name)
            else:
                self.expression_stack[-1][-1][1] = 'array'
                return False

    def check_expression_func(self, current_node, **kwargs):
        entry, _ = self.get_sym_table_entry(current_node.token_value)
        if entry is not None:
            if entry.attributes['dec-type'] == 'function' and entry.type == 'void':
                if len(self.expression_stack) > 1 or len(self.expression_stack[-1]) > 1:
                    self.err("operand_mismatch")

    def end_secondary_expression_check(self, *args, **kwargs):
        expr = self.expression_stack[-1]
        for ent in expr:
            item = ent[0]
            if item == Token(CTokenType.ID):
                item, _ = self.get_sym_table_entry(item.token_value)
                if item is not None:
                    if item.attributes['dec-type'] == 'function' and item.type == 'void':
                        self.err("operand_mismatch")
                    if 'var-size' in item.attributes and ent[1] is None and len(expr) > 1:
                        self.err("invalid_index", item.name)

        self.expression_stack.pop()

    def check_void_function(self, *args, **kwargs):
        if self.function_stack[-1].type != "void":
            self.err("int_function_no_ret_val", self.function_stack[-1].name)
        elif len(self.function_stack) == 0:
            self.err("return")

    def end_function(self, *args, **kwargs):
        self.function_stack.pop()

    def check_not_void(self, *args, **kwargs):
        if self.function_stack[-1].type == "void":
            self.err("void_function_ret_val", self.function_stack[-1].name)
        elif len(self.function_stack) == 0:
            self.err("return")

    def check_func(self, current_node, **kwargs):
        name = current_node.token_value
        entry, _ = self.get_sym_table_entry(name)
        if entry.attributes['dec-type'] != "function":
            self.err("non-function", name)
