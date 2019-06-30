from ActionSymbol import ActionSymbol, MemoryAccessDirectiveObj, StackPush, VariableDirectiveObj, \
    ConstructiveActionSymbol, PBAssign


def _c(*args):
    return ConstructiveActionSymbol(args)


def _m(value, access_type=""):
    return MemoryAccessDirectiveObj(value, access_type)


def _v(var_type, **kwargs):
    return VariableDirectiveObj(var_type, **kwargs)


OP_PUSH = _c(StackPush(_v("ln", index=None))) #todo add final indices
ADDOP = _c(PBAssign(_m(_v("pc", index=2)), _m(_v("ss", index=0)), _m(_v("ss", index=0)), _m(_v("ss", index=1)), _m(_v("ss", index=2))))
# MULT = _c(PBAssign(_v))


