from ActionSymbol import MemoryAccessDirectiveObj


def _m(value, access_type=""):
    return MemoryAccessDirectiveObj(value, access_type)


class ActivationRecord:
    control_link = 1
    access_link = 2
    temp_count = 0

    def __init__(self, func_name):
        self.func_name = func_name
        self.params = 0
        self.locals = 0
        self.array_stack = []
        # self.top_sp = top_sp
        # self.create_table()

    def add_param(self):
        self.params += 1

    def add_local(self, cg):
        self.locals += 1

    def after_local(self, cg):
        table = cg.get_int_vars(self.func_name)
        fp = self.get_temp()
        cg.add_pc(1)
        cg.pb[cg.pc - 1] = "ASSIGN", _m(cg.top_sp), fp
        t = self.get_temp()
        for i, entry in table:
            if 'var-size' in entry.attributes:
                cg.add_pc(3)
                cg.pb[cg.pc - 3] = "ADD", _m(cg.top_sp), _m(i + ActivationRecord.control_link + ActivationRecord.access_link, "#"), _m(t)
                cg.pb[cg.pc - 2] = "ASSIGN", _m(cg.top_sp), _m(t)
                cg.pb[cg.pc - 1] = "ADD", _m(cg.top_sp), _m(entry.attributes['var-size'], '#'), _m(cg.top_sp)
        cg.add_pc(1)
        cg.pb[cg.pc - 1] = "ASSIGN", _m(fp), cg.top_sp


    def find_ptr(self, name, cg):
        _, i = cg.semantics.symbol_table.get_sym_table_funcless_entry(name)
        al_loc = ActivationRecord.control_link
        t = cg.get_temp()
        t2 = cg.get_temp()
        al = cg.get_temp()
        cg.add_pc(9)
        cg.pb[cg.pc - 9] = "ADD", _m(al_loc * 4, "#"), _m(cg.top_sp), _m(al)
        cg.pb[cg.pc - 8] = "JP", _m(cg.pc + 2)
        cg.pb[cg.pc - 7] = "ASSIGN", _m(al, "@"), _m(al)
        cg.pb[cg.pc - 6] = "ADD", _m(4, "#"), _m(al), _m(t)
        cg.pb[cg.pc - 5] = "ASSIGN", _m(t, "@"), _m(t)
        cg.pb[cg.pc - 4] = "LT", _m(t), _m(i, "#"), _m(t2)
        cg.pb[cg.pc - 3] = "JPF", _m(t2), _m(cg.pc - 5)
        cg.pb[cg.pc - 2] = "SUB", _m(i + (al_loc + ActivationRecord.access_link), "#"), _m(t), _m(t)
        cg.pb[cg.pc - 1] = "ADD", _m(cg.top_sp), _m(t), _m(t)
        # maybe free t?
        return t

    # def organize_temps(self, cg):
    #     self.pb[self.ss_i(0)] = "ADD", _m(self.top_sp), _m(len(self.get_top_ar().temps), "#"), _m(self.top_sp)
    #     self.pop(1)
    #     for code in self.pb:
    #         if code:
    #             for value in code:
    #                 for temp in self.get_top_ar().temps():
    #                     if temp in value:
    #                         offset = int(temp[4:])


