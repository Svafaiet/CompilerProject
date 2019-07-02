from ActivationRecord import ActivationRecord
from ActionSymbol import MemoryAccessDirectiveObj


def _m(value, access_type=""):
    return MemoryAccessDirectiveObj(value, access_type)


class CodeGenerator:
    INIT_PC_VALUE = 0
    INIT_MEMORY_VALUE = 500
    REGISTER_SIZE = 200

    def __init__(self, semantics, file_out):
        self.semantics = semantics
        self.file_out = file_out
        self.ss = []
        self.pb = [None] * CodeGenerator.INIT_PC_VALUE
        self.pc = CodeGenerator.INIT_PC_VALUE
        self.top_sp = CodeGenerator.INIT_MEMORY_VALUE
        self.ar_stack = []
        self.call_stack = []
        self.temp_set = set()

        """
        with entries:
            ("while", []: a list of break and continues belong to this while, while_condition_label),
            ("switch", []: a list of breaks belong to this switch, None)
        """
        self.while_switch_stack = []

        self.init_cg()

    def init_cg(self):
        """
        initial memory organization
        output
        call main
        :return:
        """
        self.add_pc(1)
        self.pb[self.pc - 1] = "ASSIGN", _m(CodeGenerator.REGISTER_SIZE + CodeGenerator.INIT_MEMORY_VALUE, "#"), _m(
            self.top_sp)
        self.init_global_func()
        self.save()  # control_link at end of
        self.save()  # for j main
        self.make_output()

    def init_global_func(self):
        self.push("__global__")
        global_ar = ActivationRecord("__global__", -1)
        self.semantics.set_ar(global_ar)
        self.ar_stack.append(global_ar)
        self.use_ar()
        self.pb[self.ss_i(0)] = "ASSIGN", _m(self.pc, "#"), _m(self.top_sp, "@")

    def make_output(self):
        self.push("output")
        output_ar = ActivationRecord("output", -2)
        self.semantics.set_ar(output_ar)
        self.ar_stack.append(output_ar)
        self.add_param()
        self.use_ar()
        self.pb[self.ss_i(0)] = "ASSIGN", _m(self.pc, "#"), _m(self.top_sp, "@")
        self.add_pc(1)
        # todo  fix fp
        self.pb[self.pc - 1] = "PRINT", _m(self.top_sp, "@")
        self.end_local()
        self.end_function()

    def add_pc(self, offset):
        self.pb += [None] * offset
        self.pc += offset

    def get_temp(self):
        for i in range(1, int(CodeGenerator.REGISTER_SIZE / 4)):
            reg = CodeGenerator.INIT_MEMORY_VALUE + 4 * (i + 1)
            if not (reg in self.temp_set):
                self.temp_set.add(reg)
                return reg

    def free_temp(self, val):
        self.temp_set.remove(val)

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

    def get_top_call(self):
        return self.call_stack[-1]

    def get_int_vars(self, func_name):
        _, i = self.semantics.get_sym_table_entry(func_name)
        return list(filter(lambda x: (x.attributes['dec-type'] != "function"), self.semantics.symbol_table[i:]))

    def reset_temp(self):
        """
        with assumption of fp not being in fp, put all Reg_size in SP
        """
        i = self.get_temp()
        t = self.get_temp()
        fp = self.get_temp()
        self.add_pc(1)
        self.pb[self.pc - 1] = "ASSIGN", _m(self.top_sp, "@"), _m(fp)
        self.add_pc(6)
        self.pb[self.pc - 6] = "ASSIGN", _m(CodeGenerator.INIT_MEMORY_VALUE, "#"), _m(i)
        self.pb[self.pc - 5] = "ADD", _m(i), _m(4, "#"), _m(i)
        self.pb[self.pc - 4] = "ADD", _m(self.top_sp), _m(4, "#"), _m(self.top_sp)
        self.pb[self.pc - 3] = "ASSIGN", _m(i), _m(self.top_sp, "@")
        self.pb[self.pc - 2] = "LT", _m(CodeGenerator.INIT_MEMORY_VALUE + CodeGenerator.REGISTER_SIZE, "#"), _m(i), _m(
            t)
        self.pb[self.pc - 1] = "JPF", _m(t), _m(self.pc - 5)
        self.add_pc(1)
        self.pb[self.pc - 1] = "ASSIGN", _m(fp), _m(self.top_sp, "@")
        self.free_temp(fp)
        self.free_temp(t)
        self.free_temp(i)
        # self.pb[]

    def retrieve_temp(self):
        """
        with assumption of fp not being in fp, put all Reg_size in SP
        """

        i = self.get_temp()
        j = self.get_temp()
        t = self.get_temp()
        fp = self.get_temp()
        self.add_pc(1)
        self.pb[self.pc - 1] = "ASSIGN", _m(self.top_sp, "@"), _m(fp)
        self.add_pc(7)
        self.pb[self.pc - 7] = "ADD", _m(self.top_sp), _m(+ 4, "#"), _m(j)
        self.pb[self.pc - 6] = "ASSIGN", _m(CodeGenerator.INIT_MEMORY_VALUE + 4, "#"), _m(i)
        self.pb[self.pc - 5] = "ADD", _m(i), _m(CodeGenerator.INIT_MEMORY_VALUE + 4, "#"), _m(i)
        self.pb[self.pc - 4] = "ASSIGN", _m(i), _m(self.top_sp, "@")
        self.pb[self.pc - 3] = "ADD", _m(self.top_sp), _m(4, "#"), _m(self.top_sp)
        self.pb[self.pc - 2] = "LT", _m(CodeGenerator.INIT_MEMORY_VALUE + CodeGenerator.REGISTER_SIZE, "#"), _m(i), _m(
            t)
        self.pb[self.pc - 1] = "JPF", _m(t), _m(self.pc - 5)
        self.add_pc(1)
        self.pb[self.pc - 1] = "ASSIGN", _m(fp), _m(self.top_sp, "@")
        self.free_temp(fp)
        self.free_temp(t)
        self.free_temp(j)
        self.free_temp(i)

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
        action_routine(current_node, **kwargs)
        try:
            pass
        except Exception as e:
            print(e)

    def pop_ss(self, *args, **kwargs):
        t = self.pop(1)
        self.free_temp(t)

    def push_tok(self, current_node, **kwargs):
        self.push(current_node.token_value)

    def push_num(self, current_node, **kwargs):
        t = self.get_temp()
        self.add_pc(1)
        self.pb[self.pc - 1] = "ASSIGN", _m(current_node.token_value, "#"), _m(t)
        self.push(t)

    def push_dummy(self, *args, **kwargs):
        t = self.get_temp()
        self.push(t)

    def pid(self, *args, **kwargs):
        """
        pop id_tok_value from stack and put a temp which contains id_tok_value address in memory
        """
        self.push(self.get_top_ar().find_ptr(self.pop(1), self))

    def val_at(self, *args, **kwargs):
        """
        take address at top of stack and put value of address in address temp
        """
        self.add_pc(1)
        self.pb[self.pc - 1] = "ASSIGN", _m(self.ss_i(0), "@"), _m(self.ss_i(0))

    def assignment(self, *args, **kwargs):
        self.add_pc(1)
        t = self.ss_i(0)
        self.pb[self.pc - 1] = "ASSIGN", _m(self.ss_i(0)), _m(self.ss_i(1), "@")
        self.pop(2)
        self.push(t)

    def math_bin_op(self, *args, **kwargs):
        tok_to_icg = {
            "+": "ADD",
            "-": "SUB",
            "*": "MULT",
        }
        self.add_pc(1)
        self.pb[self.pc - 1] = tok_to_icg[self.ss_i(1)], _m(self.ss_i(2)), _m(self.ss_i(0)), _m(self.ss_i(2))
        self.pop(2)

    def math_unary_op(self, *args, **kwargs):
        tok_to_icg = {
            "+": "ADD",
            "-": "SUB",
        }
        val = self.pop()
        self.add_pc(1)
        self.pb[self.pc - 1] = tok_to_icg[self.ss_i(1)], _m(0, "#"), _m(val), _m(val)
        self.pop()
        self.push(val)

    def bool_op(self, *args, **kwargs):
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
        self.add_pc(2)
        self.pb[self.pc - 2] = "MULT", _m(4, "#"), _m(self.ss_i(0)), _m(self.ss_i(0))
        self.pb[self.pc - 1] = "ADD", _m(self.ss_i(0)), _m(self.ss_i(1)), _m(self.ss_i(1))
        self.pop(1)
        # self.pb[self.pc - 1] = "ASSIGN", _m(self.ss_i(0), "@"), _m(self.ss_i(0))

    def add_param(self, *args, **kwargs):
        top_ar = self.get_top_ar()
        top_ar.add_param()

    def add_local(self, *args, **kwargs):
        top_ar = self.get_top_ar()
        top_ar.add_local()

    def add_local_arr_len(self, *args, **kwargs):
        # top_ar = self.get_top_ar()
        # top_ar.add_size(self)
        pass

    def after_local(self):
        # set fp
        self.add_pc(1)
        self.pb[self.pc - 1] = "SUB", _m(self.top_sp), _m(self.get_top_ar().get_const_size(), "#"), _m(self.top_sp, "@")

    def call_start(self, *args, **kwargs):
        self.use_ar()

    def call_end(self, *args, **kwargs):
        entry = self.semantics.get_sym_table_entry(self.ss_i(1))[0]
        self.add_pc(1)
        self.pb[self.pc - 1] = "JP", _m(entry.attributes["ar"].func_line)
        self.pb[self.ss_i(0)] = "ASSIGN", _m(self.pc, "#"), _m(self.top_sp, "@")
        self.pop(2)
        if entry.type != "void":
            t = self.get_temp()
            self.add_pc(2)
            self.pb[self.pc - 2] = "ADD", _m(entry.attributes["ar"].return_cnt * 4, "#"), _m(self.top_sp), _m(t)
            self.pb[self.pc - 1] = "ASSIGN", _m(t, "@"), _m(t)
            self.push(t)

    def call_arg(self, *args, **kwargs):
        self.add_pc(2)
        self.pb[self.pc - 2] = "ADD", _m(self.top_sp), _m(4, "#"), _m(self.top_sp)
        self.pb[self.pc - 1] = "ASSIGN", _m(self.ss_i(0)), _m(self.top_sp, "@")
        self.pop(1)

    # todo handle local arrays

    def use_ar(self):
        # 8 pc passed, one poped
        entry, _ = self.semantics.get_sym_table_entry(self.ss_i(0))
        ar = entry.attributes['ar']
        prev_ar = self.get_top_ar()
        self.add_pc(10)
        after_sp_ptr = self.get_temp()
        self.pb[self.pc - 10] = "ADD", _m(self.top_sp), _m(4 * ar.return_cnt, "#"), _m(self.top_sp)
        self.pb[self.pc - 9] = "ADD", _m(self.top_sp), _m(4, "#"), _m(self.top_sp)
        # self.pb[self.pc - 7] = "ASSIGN", _m(control_link, "#"), _m(self.top_sp, "@")
        self.push(self.pc - 8)
        self.pb[self.pc - 7] = "ADD", _m(self.top_sp), _m(4, "#"), _m(after_sp_ptr)
        self.pb[self.pc - 6] = "SUB", _m(self.top_sp), _m(4 + 4 * ar.return_cnt, "#"), _m(self.top_sp)
        al_loc = ActivationRecord.control_link
        self.pb[self.pc - 5] = "ADD", _m(al_loc * 4, "#"), _m(self.top_sp), _m(after_sp_ptr, "@")
        self.pb[self.pc - 4] = "ADD", _m(after_sp_ptr), _m(4, "#"), _m(after_sp_ptr)
        al_size = len(self.get_int_vars("__global__")) - len(self.get_int_vars(self.ss_i(0)))
        self.pb[self.pc - 3] = "ASSIGN", _m(al_size, "#"), _m(after_sp_ptr, "@")
        self.pb[self.pc - 2] = "ADD", _m(after_sp_ptr), _m(4 * (ar.variable_size() + 1), "#"), _m(after_sp_ptr)
        self.pb[self.pc - 1] = "ASSIGN", _m(after_sp_ptr), _m(self.top_sp)

    def start_function(self, *args, **kwargs):
        ar = ActivationRecord(self.ss_i(0), self.pc)
        self.ar_stack.append(ar)
        self.semantics.set_ar(ar)

    def end_local(self, *args, **kwargs):
        ar = self.ar_stack[-1]
        ar.arr_memory(self)
        self.reset_temp()
        self.call_stack.append(self.temp_set)
        self.temp_set = set()

    def end_function(self, *args, **kwargs):
        self.ar_stack.pop()
        self.temp_set = self.call_stack.pop()

    """return"""
    def remove_ar(self, *args, **kwargs):
        self.add_pc(1)
        self.pb[self.pc - 1] = "ASSIGN", _m(self.top_sp, "@"), _m(self.ss_i(0))
        self.pop(1)
        self.add_pc(1)
        self.pb[self.pc - 1] = "ADD", _m(self.top_sp, "@"), _m(self.get_top_ar().return_cnt * 4, "#"), _m(self.top_sp)
        self.retrieve_temp()
        pass

    def set_return(self, *args, **kwargs):
        t = self.get_temp()
        self.add_pc(2)
        self.pb[self.pc - 2] = "ASSIGN", _m(self.top_sp, "@"), _m(t)
        self.pb[self.pc - 1] = "SUB", _m(self.top_sp), _m(4 + 4 * self.get_top_ar().return_cnt, "#"), _m(self.top_sp)
        self.free_temp(t)  # danger
        self.add_pc(1)
        self.pb[self.pc - 1] = "JP", _m(t, "@")

    def jp_save(self, *args, **kwargs):
        """
            first jumps by 2
            saves the previous address(pushes to stack)
            later fills the saved address with a jump to the end of switch
        :param args:
        :param kwargs:
        :return:
        """
        self.while_switch_stack.append(("switch", []))
        self.add_pc(2)
        self.pb[self.pc - 2] = "JP", _m(self.pc)
        self.push(self.pc - 1)

    def comp_save(self, *args, **kwargs):
        """
            compares the switch expression with case NUM
            saves current address and the result of comparison (pushes to stack)
            later fills the saved address with a jumpF to the next case
        :param args:
        :param kwargs:
        :return:
        """
        t = self.get_temp()
        self.add_pc(2)
        self.pb[self.pc - 2] = "EQ", _m(self.ss_i(0)), _m(self.ss_i(1)), _m(t)
        self.pop(1)
        self.push(t)
        self.push(self.pc - 1)

    def back_patch(self, *args, **kwargs):
        """
            fills the saved address from a case with a jump false
        :param args:
        :param kwargs:
        :return:
        """
        self.pb[self.ss_i(0)] = "JPF", _m(self.ss_i(1)), _m(self.pc)
        self.pop(2)

    def end_switch(self, *args, **kwargs):
        """
            fills the address saved before switch with a jump to current address (outside switch)
        :param args:
        :param kwargs:
        :return:
        """
        self.pb[self.ss_i(1)] = "JP", _m(self.pc)
        self.pop(2)
        self.fill_breaks(*args, **kwargs)

    def print_code(self):
        with open(file=self.file_out, mode="w") as f:
            for i, instruction in enumerate(self.pb):
                if not instruction: #todo
                    continue
                inst = "{}  ".format(i)
                for operand in instruction:
                    if isinstance(operand, str):
                        inst += "({}".format(operand)
                    elif isinstance(operand, MemoryAccessDirectiveObj):
                        inst += ", {}{}".format(operand.access_type, operand.value)
                inst += ")\n"
                f.write(inst)

    def fill_breaks(self, *args, **kwargs):
        entry = self.while_switch_stack[-1]
        if len(entry[1]) > 0:
            for i in entry[1]:
                self.pb[i] = "JP", _m(self.pc)
        self.while_switch_stack.pop()
