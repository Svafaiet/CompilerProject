class ActivationRecord:
    def __init__(self, top_sp, table):
        self.control_link = None
        self.access_link = None
        self.ret_val = None
        self.params = []
        self.locals = []
        self.type = None
        self.size_place = None
        self.size = 0
        self.temps = []
        self.fp = None
        self.top_sp = top_sp
        self.create_table()

    def find_ptr(self, code_generator):
        semantics = code_generator.semantics
        pc = code_generator.pc
        pb = code_generator.pb
        symtable = semantics.symbol_table



