from CodeGenerator import _m


class ActivationRecord:
    control_link = 1
    access_link = 2

    def __init__(self):
        self.params = 0
        self.locals = 0
        self.temps = []
        # self.top_sp = top_sp
        # self.create_table()

    def make_from_ar(self, ar):
        self.add_pc()
        after_sp_ptr = ar.get_temp()
        self.pb[self.pc] = "ADD", _m(self.top_sp), _m(4, "#"), _m(after_sp_ptr)
        self.pb[self.pc] = "ASSIGN", _m(self.pc, "#"), _m(after_sp_ptr)
        self.pb[self.pc] = "ADD", _m(after_sp_ptr), _m(4, "#"), _m(after_sp_ptr)
        al_loc = ActivationRecord.control_link + ActivationRecord.access_link - 1
        self.pb[self.pc] = "ADD", _m(al_loc * 4, "#"), _m(self.top_sp), _m(after_sp_ptr)
        self.pb[self.pc] = "ADD", _m(after_sp_ptr), _m(4, "#"), _m(after_sp_ptr)
        _, al_size = self.semantics.get_sym_table_entry(self.ss_i(0)) + 1
        self.pop(1)
        self.pb[self.pc] = "ASSIGN", _m(al_size, "#"), _m(after_sp_ptr)

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
        al_loc = ActivationRecord.control_link + ActivationRecord.access_link - 1
        t = self.get_temp()
        al = self.get_temp()
        cg.add_pc(7)
        cg.pb[cg.pc - 7] = "ADD", _m(al_loc * 4, "#"), _m(cg.top_sp), _m(al)
        cg.pb[cg.pc - 6] = "JP", _m(cg.pc + 2)
        cg.pb[cg.pc - 5] = "ASSIGN", _m(al, "@"), _m(al)
        cg.pb[cg.pc - 4] = "ADD", _m(4, "#"), _m(al), _m(t)
        cg.pb[cg.pc - 3] = "ASSIGN", _m(t, "@"), _m(t)
        cg.pb[cg.pc - 2] = "LT", _m(t), _m(i, "#"), _m(t)
        cg.pb[cg.pc - 1] = "JPF", _m(t), _m(cg.pc - 5)
        # maybe free t?
        return t


#TODO end function handle arr pointers/