from CodeGenerator import _m


class ActivationRecord:
    control_link = 1
    access_link = 2

    def __init__(self, func_name):
        self.func_name = func_name
        self.params = 0
        self.locals = 0
        self.temps = []
        # self.top_sp = top_sp
        # self.create_table()

    def get_temp(self):
        new_temp = "TEMP" + str(len(self.temps))
        self.temps.append(new_temp)
        return new_temp

    def add_param(self):
        self.params += 1

    def add_local(self):
        self.locals += 1

    def after_local(self):
        pass

    def add_size(self, cg):
        pass

    def find_ptr(self, name, cg):
        _, i = cg.semantics.symbol_table.get_sym_table_entry(name)
        al_loc = ActivationRecord.control_link
        t = self.get_temp()
        t2 = self.get_temp()
        al = self.get_temp()
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


#TODO end function handle arr pointers/