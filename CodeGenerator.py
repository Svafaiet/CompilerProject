from ActivationRecord import ActivationRecord
from ActionSymbol import MemoryAccessDirectiveObj


def _m(value, access_type=""):
    return MemoryAccessDirectiveObj(value, access_type)


class CodeGenerator:
    INIT_PC_VALUE = 0
    INIT_MEMORY_VALUE = 500
    REGISTER_SIZE = 2000

    def __init__(self, semantics, file_out):
        self.semantics = semantics
        self.file_out = file_out
        self.ss = []
        self.pb = [None] * CodeGenerator.INIT_PC_VALUE
        self.pc = CodeGenerator.INIT_PC_VALUE
        self.top_sp = CodeGenerator.INIT_MEMORY_VALUE
        self.ar_stack = []

        """
        with entries:
            ("while", []: a list of break and continues belong to this while, while_condition_label),
            ("switch", []: a list of breaks belong to this switch, None)
        """
        self.while_switch_stack = []

    def init_cg(self):
        """
        initial memory organization
        output
        call main
        :return:
        """
        self.add_pc(1)
        self.pb[self.pc - 1] = "ASSIGN", _m(CodeGenerator.REGISTER_SIZE + CodeGenerator.INIT_MEMORY_VALUE ,"#")
        self.make_output()
        self.save() # control_link at end of
        self.save() # for j main

    def make_output(self):
        pass


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
        for entry in self.while_switch_stack[::-1]:
            if entry[0] == "while":
                self.add_pc(1)
                self.pb[self.pc - 1] = "JP", _m(entry[2])
                break

    def add_break(self, *args, **kwargs):
        self.add_pc(1)
        self.while_switch_stack[len(self.while_switch_stack) - 1][1].append(self.pc - 1)

    def get_top_ar(self):
        return self.ar_stack[-1]

    def get_int_vars(self, func_name):
        _, i = self.semantics.get_sym_table_entry(func_name)
        return list(filter(lambda x: (x.attributes['dec-type'] != "function"), self.semantics.symbol_table[i:]))

    def get_temp(self):
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

    def pop_tok(self, *args, **kwargs):
        self.pop(1)

    def push_tok(self, current_node, **kwargs):
        self.push(current_node.token_value)

    def push_num(self, current_node, **kwargs):
        t = self.get_temp()
        self.add_pc(1)
        self.pb[self.pc - 1] = "ASSIGN", _m(current_node.token_value, "#"), _m(t)
        self.push(t)
        # todo for arr decleration
        # fixme

    def math_bin_op(self, current_node, **kwargs):
        tok_to_icg = {
            "+": "ADD",
            "-": "SUB",
            "*": "MULT",
        }
        self.add_pc(1)
        self.pb[self.pc - 1] = tok_to_icg[self.ss_i(1)], _m(self.ss_i(2)), _m(self.ss_i(0)), _m(self.ss_i(2))
        self.pop(2)

    def math_unary_op(self, current_node, **kwargs):
        tok_to_icg = {
            "+": "ADD",
            "-": "SUB",
        }
        val = self.pop()
        self.add_pc(1)
        self.pb[self.pc - 1] = tok_to_icg[self.ss_i(1)], _m(0, "#"), _m(val), _m(val)
        self.pop()
        self.push(val)

    def bool_op(self, current_node, **kwargs):
        tok_to_icg = {
            "==": "EQ",
            "<": "LT",
            ">": "LT"
        }
        self.add_pc(1)
        if self.ss_i(1) == ">":
            self.pb[self.pc - 1] = tok_to_icg[self.ss_i(1)], _m(self.ss_i(0)), _m(self.ss_i(2)), _m(self.ss_i(2))
        else:
            self.pb[self.pc - 1] = tok_to_icg[self.ss_i(1)], _m(self.ss_i(2)), _m(self.ss_i(0)), _m(self.ss_i(2))
        self.pop(2)

    def save(self, *args, **kwargs):
        self.push(self.pc)
        self.add_pc(1)

    def label(self, *args, **kwargs):
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
        self.add_pc(1)
        self.pb[self.pc - 1] = "JP", _m(self.ss_i(2))
        self.pop(3)

    def switch_start(self):
        self.push(self.pc)
        self.add_pc(1)
        # todo

    def calc_arr(self, *args, **kwargs):
        self.add_pc(3)
        self.pb[self.pc - 3] = "MULT", _m(4, "#"), _m(self.ss_i(0)), _m(self.ss_i(0))
        self.pb[self.pc - 2] = "ADD", _m(self.ss_i(0)), _m(self.ss_i(1)), _m(self.ss_i(1))
        self.pop()
        self.pb[self.pc - 1] = "ASSIGN", _m(self.ss_i(0), "@"), _m(self.ss_i(0))

    def add_param(self, current_node, **kwargs):
        top_ar = self.get_top_ar()
        top_ar.add_param()

    def add_local(self, *args, **kwargs):
        top_ar = self.get_top_ar()
        top_ar.add_local(self)

    def add_local_arr_len(self, *args, **kwargs):
        top_ar = self.get_top_ar()
        top_ar.add_size(self)

    # def after_l

    def call(self, *args, **kwargs):
        self.make_ar(self.pc + 9)

    def call_arg(self, *args, **kwargs):
        self.add_pc(2)
        self.pb[self.pc - 2] = "ASSIGN", _m(self.top_sp), _m(self.ss_i(0))
        self.pop(1)
        self.pb[self.pc - 1] = "ADD", _m(self.top_sp), _m()

    def make_ar(self, control_link):
        self.add_pc(9)
        after_sp_ptr = self.get_temp()
        self.pb[self.pc - 9] = "ADD", _m(self.top_sp), _m(4, "#"), _m(after_sp_ptr)
        self.pb[self.pc - 8] = "ASSIGN", _m(control_link, "#"), _m(after_sp_ptr, "@")
        self.pb[self.pc - 7] = "ADD", _m(after_sp_ptr), _m(4, "#"), _m(after_sp_ptr)
        al_loc = ActivationRecord.control_link
        self.pb[self.pc - 6] = "ADD", _m(al_loc * 4, "#"), _m(self.top_sp), _m(after_sp_ptr, "@")
        self.pb[self.pc - 5] = "ADD", _m(after_sp_ptr), _m(4, "#"), _m(after_sp_ptr)
        _, al_size = self.semantics.get_int_vars(self.ss_i(0)) + 1
        self.pop(1)
        self.pb[self.pc - 4] = "ASSIGN", _m(al_size, "#"), _m(after_sp_ptr, "@")
        self.pb[self.pc - 3] = "ADD", _m(after_sp_ptr), _m(4, "#"), _m(after_sp_ptr)
        self.pb[self.pc - 1] = "ASSIGN", _m(after_sp_ptr), _m(self.top_sp)
        self.ar_stack.append(ActivationRecord(self.ss_i(0)))

    # todo handle local arrays

    def end_function(self, *args, **kwargs):
        self.get_top_ar().after_local()
        self.pb[self.ss_i(0)] = "ADD", _m(self.top_sp), _m(len(self.get_top_ar().temps), "#"), _m(self.top_sp)
        self.pop(1)
        for code in self.pb:
            if code:
                for value in code:
                    for temp in self.get_top_ar().temps():
                        if temp in value:
                            offset = int(temp[4:])



        self.ar_stack.pop()

