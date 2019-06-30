from ActionSymbol import MemoryAccessDirectiveObj


def _m(value, access_type=""):
    return MemoryAccessDirectiveObj(value, access_type)


class CodeGenerator:
    INIT_PC_VALUE = 0

    def __init__(self, semantics, file_out):
        self.semantics = semantics
        self.file_out = file_out
        self.ss = []
        self.pb = [None] * CodeGenerator.INIT_PC_VALUE
        self.pc = CodeGenerator.INIT_PC_VALUE

        """
        with entries:
            ("while", []: a list of break and continues belong to this while, while_condition_label),
            ("switch", []: a list of breaks belong to this switch, None)
        """
        self.while_switch_stack = []

    def add_pc(self, offset):
        self.pb += [None] * offset
        self.pc += offset

    def get_temp(self):
        pass

    def push(self, value):
        self.ss.append(value)

    def pop(self, count=1):
        if count > 1:
            self.ss.pop()
            return self.pop(count - 1)
        return self.ss.pop()

    def ss_i(self, i):
        return self.ss[len(self.ss) - 1 - i]

    """
    while_switch_stack methods
    """
    def add_continue(self):
        pass

    def handle_action_symbol(self, action_symbol, **kwargs):
        current_node = kwargs.pop('current_node', None)
        action_symbol_type = action_symbol.type
        action_routine = None
        if current_node is None and action_symbol_type != "scope_end":
            if action_symbol_type == 'DECLARE_TYPE':
                self.prev_sym_entry = None
            # Todo handle errors
            return
        action_routine = eval("self." + action_symbol_type.lower())
        try:
            action_routine(current_node, **kwargs)
        except Exception as e:
            print(e)

    def push_tok(self, current_node, **kwargs):
        self.push(current_node.token_value)

    def push_num(self, current_node, **kwargs):
        t = self.get_temp()
        self.pb[self.pc] = "ASSIGN", _m(current_node.token_value, "#"), _m(t)
        self.add_pc(1)
        self.push(t)

    def math_bin_op(self, current_node, **kwargs):
        tok_to_icg = {
            "+": "ADD",
            "-": "SUB",
            "*": "MULT",
        }
        self.pb[self.pc] = tok_to_icg[self.ss_i(1)], _m(self.ss_i(2)), _m(self.ss_i(0)), _m(self.ss_i(2))
        self.pop(2)

    def math_unary_op(self, current_node, **kwargs):
        tok_to_icg = {
            "+": "ADD",
            "-": "SUB",
        }
        val = self.pop()
        self.pb[self.pc] = tok_to_icg[self.ss_i(1)], _m(0, "#"), _m(val), _m(val)
        self.pop()
        self.push(val)

    def bool_op(self, current_node, **kwargs):
        tok_to_icg = {
            "==": "EQ",
            "<": "LT",
            ">": "LT"
        }
        if self.ss_i(1) == ">":
            self.pb[self.pc] = tok_to_icg[self.ss_i(1)], _m(self.ss_i(0)), _m(self.ss_i(2)), _m(self.ss_i(2))
        else:
            self.pb[self.pc] = tok_to_icg[self.ss_i(1)], _m(self.ss_i(2)), _m(self.ss_i(0)), _m(self.ss_i(2))
        self.pop(2)

    def save(self, current_node, **kwargs):
        self.push(self.pc)
        self.add_pc(1)

    def label(self, current_node, **kwargs):
        self.push(self.pc)

    def else_start(self, current_node, **kwargs):
        self.pb[self.ss_i(0)] = "JPF", _m(self.ss_i(1)), _m(self.pc + 1)
        self.pop(2)
        self.save(current_node, **kwargs)

    def else_end(self, current_node, **kwargs):
        self.pb[self.ss_i(0)] = "JP", _m(self.pc)
        self.pop()

    def while_start(self, current_node, **kwargs):
        self.label(current_node, kwargs)
        self.while_switch_stack.append(("while", [], self.ss_i(0)))

    def while_save(self, current_node, **kwargs):
        self.pb[self.ss_i(0)] = "JPF", _m(self.ss_i(1)), _m(self.pc + 1)
        self.pb[self.pc] = "JP", _m(self.ss_i(2))
        self.add_pc(1)
        self.pop(3)

    def switch_start(self):
        self.push(self.pc)
        self.add_pc(1)
        # todo

    def calc_arr(self, current_node, **kwargs):
        self.pb[self.pc] = "MULT", _m("4", "#"), _m(self.ss_i(0)), _m(self.ss_i(0))
        self.pb[self.pc + 1] = "ADD", _m(self.ss_i(0)), _m(self.ss_i(1)), _m(self.ss_i(1))
        self.pop()
        self.pb[self.pc + 2] = "ASSIGN", _m(self.ss_i(0), "@"), _m(self.ss_i(0))
        self.add_pc(3)
