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

    def add_pc(self, offset):
        self.pb += [None] * offset
        self.pc += offset

    def get_temp(self):
        pass

    def push(self, value):
        self.ss.append(value)

    def pop(self, count=0):
        if count > 0:
            self.ss.pop()
            return self.pop(count - 1)
        return self.ss.pop()

    def ss_i(self, i):
        return self.ss[len(self.ss) - 1 - i]

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

    def op_push(self, current_node, **kwargs):
        self.push(current_node.token_value)

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
        self.pb[self.pc] = tok_to_icg[self.ss_i(1)], _m(0, "#"), _m(self.ss_i(0)), _m(self.ss_i(0))

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

    def label(self, current_node, **kwargs):
        self.push(self.pc)
        self.add_pc(1)

    def if_save(self, current_node, **kwargs):
        self.pb[self.ss_i(0)] = "JPF", _m(self.pc)
        self.pop(1)

    def while_start(self, current_node, **kwargs):
        pass

    def while_save(self, current_node, **kwargs):
        self.pb[self.ss_i(0)] = "JPF", _m(self.ss_i(1)), _m(self.pc + 1)
        self.pb[self.pc] = "JP", _m(self.ss_i(2))
        self.pb[self.ss_i(3)] = "JP", _m(self.pc + 1)
        self.add_pc(1)
        self.pop(3)

    def break_stmt(self, current_node, **kwargs):
        pass

    def continue_stmt(self, current_node, **kwargs):
        pass

    def switch_start(self):
        self.push(self.pc)
        self.add_pc(1)
        # todo

    def calc_arr(self, current_node, **kwargs):
        self.pb[self.pc] = "MULT", _m("4", "#"), _m(self.ss_i(0)), _m(self.ss_i(0))
        #todo
