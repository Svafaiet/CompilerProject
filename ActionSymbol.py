class ActionSymbol:
    def __init__(self, directives):
        self.directives = directives


class Directive:
    pass


class MemoryAccessDirectiveObj:
    """
    Different kinds of (@attr type):
    "" : (@attr value)
    "#" : mem[(@attr value)]
    "@" : mem[mem[@attr value]]
    (@attr value) is VariableDirectiveObj
    """

    def __init__(self, value, type=""):
        self.type = type
        self.value = value


class VariableDirectiveObj:
    """
    "pc" : program_counter + offset (i + (@attr value))
    "ss" : ss[top + (@attr value)]
    "tv" : str of temp var name in (@attr value)
    #todo
    """

    def __init__(self, value, type=""):
        self.type = type
        self.value = value

class AddPC(Directive):
    """
    i <- i + offset code directive
    """

    def __init__(self, offset=0):
        self.offset = offset


class TempGet(Directive):
    """
    temp_name <- gettemp()
    """

    def __init__(self, temp_name="t"):
        self.temp_name = temp_name


class AddressGet(Directive):
    """
    value_name <- gettemp(input)
    """

    def __init__(self, value_name):
        self.value_name = value_name


class PBAssign(Directive):
    """
    PB[i] <- (opp, args)
    """

    def __init__(self, pb_addr, opp, args):
        self.pb_addr = pb_addr
        self.opp = opp
        self.args = args
