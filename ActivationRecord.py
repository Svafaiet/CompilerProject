from CodeGenerator import _m


class ActivationRecord:
    def __init__(self, top_sp, table):
        self.control_link = 1
        self.access_link = 2
        self.params = 0
        self.locals = 0
        self.temps = []
        # self.top_sp = top_sp
        # self.create_table()

    def find_ptr(self, code_generator):
        semantics = code_generator.semantics
        pc = code_generator.pc
        pb = code_generator.pb
        symtable = semantics.symbol_table

    def get_temp(self):
        new_temp = "TEMP" + str(len(self.temps))
        self.temps.append(new_temp)
        return new_temp

    def add_param(self):
        self.params += 1

    def add_local(self):
        self.locals += 1

    def add_size(self, cg):
        pass

    def get_pointer(self, name, cg):
        _, i = cg.semantics.symbol_table.get_sym_table_entry(name)
        al_loc = self.control_link + self.access_link - 1
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