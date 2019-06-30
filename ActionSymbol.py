from DirectiveSymbol import DirectiveSymbol


class ActionSymbol(DirectiveSymbol):
    def __init__(self, t):
        self.type = t


class ConstructiveActionSymbol(ActionSymbol):
    def __init__(self, *args):
        super().__init__("HANDLE_CONSTRUCTIVE_ACTION_SYMBOL")
        self.directives = args


class ActionDirective:
    pass


class MemoryAccessDirectiveObj:
    def __init__(self, value, access_type=""):
        """
        :param access_type:
            Different kinds of (:param type) specify how to access memory in code generation
            "#" : (:param value)
            "" : mem[(:param value)]
            "@" : mem[mem[:param value]]
        :param value: must be VariableDirectiveObj
        """
        self.access_type = access_type
        self.value = value


class VariableDirectiveObj:
    """
    "pc" : program_counter + offset (i + (:param index))
    "ss" : ss[top - (:param index)]
    "tv" : str of temp var name in (:param value)
    "ln" : if (:param index) is given, use(:param index)'th children of last node otherwise last node,
        if result was token use it token_value other wise the node itself
    """

    def __init__(self, var_type, **kwargs):
        self.var_type = var_type
        self.kwargs = kwargs


class AddPC(ActionDirective):
    """
    i <- i + offset code directive
    """

    def __init__(self, offset=0):
        self.offset = offset


class StackPush(ActionDirective):
    """
    push(value)
    value is a VariableDirectiveObj
    """

    def __init__(self, value):
        self.value = value


class StackPop(ActionDirective):
    """
    push
    """


class TempGet(ActionDirective):
    """
    temp_name <- gettemp()
    """

    def __init__(self, temp_name="t"):
        self.temp_name = temp_name


class PointerGet(ActionDirective):
    """
    value_name <- findptr(input)
    #fixme
    """

    def __init__(self, value_name):
        self.value_name = value_name


class PBAssign(ActionDirective):
    """
    PB[pb_addr] <- (opp, args)
    """

    def __init__(self, pb_addr, opp, *args):
        self.pb_addr = pb_addr
        self.opp = opp
        self.args = args
