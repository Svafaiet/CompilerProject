from ActionSymbol import MemoryAccessDirectiveObj


def _m(value, access_type=""):
    return MemoryAccessDirectiveObj(value, access_type)


class ActivationRecord:
    control_link = 1
    access_link = 2
    temp_count = 0

    def __init__(self, func_name, func_line):
        self.func_name = func_name
        self.func_line = func_line
        self.state_machine = 2000
        self.return_cnt = 1
        self.params = 0
        self.locals = 0
        self.array_stack = []
        # self.top_sp = top_sp
        # self.create_table()

    def add_param(self):
        self.params += 1

    def add_local(self):
        self.locals += 1

    def arr_memory(self, cg):
        """set arr and fp"""
        fp = cg.get_temp()
        cg.add_pc(1)
        cg.pb[cg.pc - 1] = "ASSIGN", _m(cg.top_sp, "@"), _m(fp)
        cg.add_pc(1)
        cg.pb[cg.pc - 1] = "ADD", _m(cg.top_sp), _m(4 * self.locals, "#"), _m(cg.top_sp)
        t = cg.get_temp()
        for i, entry in enumerate(table):
            if 'var-size' in entry.attributes:
                cg.add_pc(3)
                cg.pb[cg.pc - 3] = "ADD", _m(cg.top_sp, "@"), _m(4 * (i + self.pre_var_size()), "#"), _m(t)
                cg.pb[cg.pc - 2] = "ASSIGN", _m(cg.top_sp), _m(t, "@")
                cg.pb[cg.pc - 1] = "ADD", _m(cg.top_sp), _m(4 * int(entry.attributes['var-size']), '#'), _m(cg.top_sp)
        cg.add_pc(1)
        cg.pb[cg.pc - 1] = "ASSIGN", _m(fp), _m(cg.top_sp, "@")
        cg.free_temp(fp)

    def del_arr(self, cg):
        fp = cg.get_temp()
        cg.add_pc(1)
        cg.pb[cg.pc - 1] = "ASSIGN", _m(cg.top_sp, "@"), _m(fp)
        cg.add_pc(1)
        cg.pb[cg.pc - 1] = "ADD", _m(cg.top_sp), _m(4 * cg.scope_size(), "#"), _m(cg.top_sp)
        cg.add_pc(1)
        cg.pb[cg.pc - 1] = "ASSIGN", _m(fp), _m(cg.top_sp, "@")
        cg.free_temp(fp)

    def find_ptr(self, name, cg):
        i = cg.semantics.get_size_from_start(name)
        al_loc = ActivationRecord.control_link + self.return_cnt
        t = cg.get_temp()
        t2 = cg.get_temp()
        al = cg.get_temp()
        cg.add_pc(10)
        cg.pb[cg.pc - 10] = "ADD", _m(al_loc * 4, "#"), _m(cg.top_sp, "@"), _m(al)
        cg.pb[cg.pc - 9] = "JP", _m(cg.pc - 7)
        cg.pb[cg.pc - 8] = "ASSIGN", _m(al, "@"), _m(al)
        cg.pb[cg.pc - 7] = "ADD", _m(4, "#"), _m(al), _m(t)
        cg.pb[cg.pc - 6] = "ASSIGN", _m(t, "@"), _m(t)
        cg.pb[cg.pc - 5] = "LT", _m(i, "#"), _m(t), _m(t2)
        cg.pb[cg.pc - 4] = "JPF", _m(t2), _m(cg.pc - 8)
        cg.pb[cg.pc - 3] = "SUB", _m(i + ActivationRecord.access_link, "#"), _m(t), _m(t)
        cg.pb[cg.pc - 2] = "MULT", _m(4, "#"), _m(t), _m(t)
        cg.pb[cg.pc - 1] = "ADD", _m(al), _m(t), _m(t)
        cg.free_temp(al)
        cg.free_temp(t2)
        return t

    def pre_var_size(self):
        return ActivationRecord.access_link + ActivationRecord.control_link + self.return_cnt

    def variable_size(self):
        return self.params + self.locals

    # def organize_temps(self, cg):
    #     self.pb[self.ss_i(0)] = "ADD", _m(self.top_sp), _m(len(self.get_top_ar().temps), "#"), _m(self.top_sp)
    #     self.pop(1)
    #     for code in self.pb:
    #         if code:
    #             for value in code:
    #                 for temp in self.get_top_ar().temps():
    #                     if temp in value:
    #                         offset = int(temp[4:])
