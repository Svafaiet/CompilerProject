from ActionSymbol import ActionSymbol
from Production import epsilon
from SemanticSymbol import SemanticSymbol
from Token import CTokenType, Token
from DirectiveSymbol import DirectiveSymbol


def ck(keyword_name):
    return Token(CTokenType.KEYWORD, keyword_name)


def cs(symbol_name):
    return Token(CTokenType.SYMBOL, symbol_name)


def s(semantic_type):
    return SemanticSymbol(semantic_type)


def a(action_type):
    return ActionSymbol(action_type)


compressed_grammar = [
    ["program", ["declaration-list", s("CHECK_MAIN"), a("END_DEC"), a("END_SCOPE"), a("END_AND_USE_GLOBAL"), Token(CTokenType.EOF)]],
    ["declaration-list", ["declaration-list", "declaration"], epsilon],
    ["declaration", ["type-specifier", Token(CTokenType.ID), s("DECLARE_NAME"), a("PUSH_TOK"), "var-func-declaration"]],
    ["var-func-declaration", ["var-declaration", s("CHECK_VAR_TYPE"), a("POP_SS")],
     ["fun-declaration"]],
    ["var-declaration",
     [cs(";")],
     [cs("["), Token(CTokenType.NUM), s("DECLARE_VAR_SIZE"), a("ADD_LOCAL_ARR_LEN"), cs("]"), cs(";")],
     # [cs("["), "expression", s("DECLARE_VAR_SIZE"), cs("]"), cs(";")] #todo if this was not comment add push_num to prev-RHS
     ],
    ["type-specifier", [ck("int"), s("DECLARE_TYPE"), ], [ck("void"), s("DECLARE_TYPE"), ]],
    ["fun-declaration",
     [cs("("), s("FUNCTION"), a("START_FUNCTION"), s("SCOPE_START"), "params", cs(")"), "compound-stmt",  a("END_FUNCTION"), s("SCOPE_END"),
      s("END_FUNCTION")]],
    ["params", [ck("void"), s("ADD_PARAM")],
     [ck("void"), s("DECLARE_TYPE"), s("ADD_PARAM"), "param-left", "param-list"],
     [ck("int"), s("DECLARE_TYPE"), s("ADD_PARAM"), "param-left", "param-list"]],
    ["param-list", [cs(","), "param", "param-list"], epsilon],
    ["param", ["type-specifier", s("ADD_PARAM"), "param-left"]],
    ["param-left",
     [Token(CTokenType.ID), s("DECLARE_NAME"), s("CHECK_VAR_TYPE"), a("ADD_PARAM"), cs("["), s("DECLARE_VAR_SIZE"),
      cs("]")],
     [Token(CTokenType.ID), s("DECLARE_NAME"), s("CHECK_VAR_TYPE"), a("ADD_PARAM"), ]],
    ["compound-stmt",
     [cs("{"), s("SCOPE_START"), "declaration-list", a("END_DEC"), "statement-list", a("END_SCOPE"), s("SCOPE_END"),
      cs("}")]],
    ["statement-list", ["statement-list", "statement"], epsilon],
    ["statement", ["expression-stmt", ], ["compound-stmt", ], ["selection-stmt", ], ["iteration-stmt", ],
     ["return-stmt", ], ["switch-stmt", ]],
    ["expression-stmt",
     [s("BEGIN_EXPRESSION_CHECK"), "expression", s("END_EXPRESSION_CHECK"), a("POP_SS"), cs(";")],
     [ck("continue"), s("CHECK_CONTINUE"), cs(";")], [ck("break"), s("CHECK_BREAK"), a("ADD_BREAK"), cs(";")], [cs(";"), ]
     ],
    ["selection-stmt",
     [ck("if"), cs("("), s("BEGIN_EXPRESSION_CHECK"), "expression", s("END_EXPRESSION_CHECK"), a("SAVE"), cs(")"),
      s("SCOPE_START"), "statement", s("SCOPE_END"), ck("else"), a("ELSE_START"), s("SCOPE_START"), "statement",
      s("SCOPE_END"), a("ElSE_END")]
     ],
    ["iteration-stmt",
     [ck("while"), a("WHILE_START"), cs("("), s("BEGIN_EXPRESSION_CHECK"), "expression", s("END_EXPRESSION_CHECK"),
      a("SAVE"),
      cs(")"),
      s("SCOPE_START"), "statement", a("WHILE_SAVE"), s("SCOPE_END"), a("FILL_BREAKS")]],
    ["return-stmt", [ck("return"), a("PUSH_DUMMY"), a("REMOVE_AR"), cs(";"), s("CHECK_VOID_FUNCTION"), a("SET_RETURN")],
     [ck("return"), s("BEGIN_EXPRESSION_CHECK"), "expression", s("CHECK_NOT_VOID"), a("REMOVE_AR"),
      s("END_SECONDARY_EXPRESSION_CHECK"), a("SET_RETURN"), cs(";")]],
    ["switch-stmt",
     [ck("switch"), a("JP_SAVE"), cs("("), s("BEGIN_EXPRESSION_CHECK"), "expression", s("END_EXPRESSION_CHECK"), cs(")"),
      cs("{"), s("SCOPE_START"), "case-stmts", "default-stmt", s("SCOPE_END"), cs("}"), a("END_SWITCH")]],
    ["case-stmts", ["case-stmts", "case-stmt"], epsilon, ],
    ["case-stmt", [ck("case"), Token(CTokenType.NUM), a("PUSH_NUM"), a("COMP_SAVE"), cs(":"), "statement-list", a("BACK_PATCH")]],
    ["default-stmt",
     [ck("default"), cs(":"), "statement-list"],
     epsilon
     ],
    ["expression",
     [Token(CTokenType.ID), s("CHECK_SCOPE"), s("ADD_VAR_TO_EXPRESSION"), a("PUSH_TOK"), "expression-left"],
     ["simple-expression"],
     ],
    ["expression-left",
     [a("PID"), "var-left", "expression-right"],
     ["call", "term-left", "additive-expression-left", "simple-expression-left"]
     ],
    ["expression-right",
     [cs("="), "expression", a("ASSIGNMENT")],
     [a("VAL_AT"), "term-left", "additive-expression-left", "simple-expression-left"]
     ],
    ["var", [Token(CTokenType.ID), s("CHECK_SCOPE"), a("PUSH_TOK"), a("PID"), "var-left"]],
    ["var-left", [s("CHECK_ARRAY"), cs("["), s("BEGIN_EXPRESSION_CHECK"),
                  "expression", s("END_SECONDARY_EXPRESSION_CHECK"), a("CALC_ARR"), cs("]")], epsilon],
    ["simple-expression", ["additive-expression-right", "simple-expression-left"]],
    ["simple-expression-left", ["relop", "additive-expression", a("BOOL_OP")], epsilon],
    ["relop",
     [cs("<"), a("PUSH_TOK")],
     [cs("=="), a("PUSH_TOK")],
     [cs(">"), a("PUSH_TOK")]
     ],
    ["additive-expression",
     ["term", "additive-expression-left"],
     ],
    ["additive-expression-left", ["addop", "term", a("MATH_BIN_OP"), "additive-expression-left"], epsilon],
    ["additive-expression-right",
     ["signed-factor-left", "term-left", "additive-expression-left"],
     ["factor-left", "term-left", "additive-expression-left"]
     ],
    ["addop",
     [cs("+"), a("PUSH_TOK")],
     [cs("-"), a("PUSH_TOK")],
     ],
    ["term", ["signed-factor", "term-left"]],
    ["term-left", [cs("*"), a("PUSH_TOK"), "signed-factor", a("MATH_BIN_OP"), "term-left"], epsilon],
    ["signed-factor",
     ["factor"],
     ["signed-factor-left"]
     ],
    ["signed-factor-left",
     [cs("+"), a("PUSH_TOK"), "factor", a("MATH_UNARY_OP")],
     [cs("-"), a("PUSH_TOK"), "factor", a("MATH_UNARY_OP")]
     ],
    ["factor",
     [Token(CTokenType.ID), s("CHECK_SCOPE"), s("ADD_VAR_TO_EXPRESSION"), a("PUSH_TOK"), "var-call"],
     ["factor-left"]
     ],
    ["factor-left",
     [cs("("), "expression", cs(")")],
     [Token(CTokenType.NUM), s("ADD_VAR_TO_EXPRESSION"), a("PUSH_NUM")]
     ],
    ["var-call", ["var-left"], ["call"]],
    ["call", [s("CHECK_EXPRESSION_FUNC"), s("CHECK_FUNC_ARGS_BEGIN"), s("CHECK_FUNC"), a("CALL_START"), cs("("), "args",
              s("CHECK_FUNC_ARGS_END"), cs(")"), a("CALL_END")]],
    ["args",
     ["arg-list"],
     epsilon,
     ],
    ["arg-list",
     ["arg-list", cs(","), s("BEGIN_EXPRESSION_CHECK"), "expression", s("END_SECONDARY_EXPRESSION_CHECK"), s("ARG"), a("CALL_ARG")],
     [s("BEGIN_EXPRESSION_CHECK"), "expression", s("END_SECONDARY_EXPRESSION_CHECK"), s("ARG"), a("CALL_ARG")],
     ],
]
