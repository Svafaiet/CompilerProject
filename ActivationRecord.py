from CodeGenerator import _m


class ActivationRecord:
    def __init__(self, top_sp, table):
        self.control_link = 1
        self.access_link = 2
        self.params = 0
        self.locals = 0
        self.size_place = 1
        self.size = 0
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
        cg.pb[cg.pc] = "MULT", _m(cg.ss_i(0)), _m(4, "#"), _m(cg.ss_i(0))
        t = self.get_temp()
        size_pointer = self.control_link + self.access_link + self.params + self.locals
        cg.pb[cg.pc + 1] = "ADD", _m(cg.top_sp, "@"), _m(
            size_pointer, "#"), t
        cg.pb[cg.pc + 2] = "ADD", _m(t), _m(cg.ss_i(0)), _m(t)
