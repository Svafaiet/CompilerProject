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


compressed_grammar = [
    ["program", ["declaration-list", Token(CTokenType.EOF)]],
    ["declaration-list", ["declaration-list", "declaration"], epsilon],
    ["declaration", ["type-specifier", Token(CTokenType.ID), s("DECLARE_NAME"), "var-func-declaration"]],
    ["var-func-declaration", ["var-declaration", ], ["fun-declaration"]],
    ["var-declaration",
     [cs(";")],
     [cs("["), Token(CTokenType.NUM), s("DECLARE_VAR_SIZE"), cs("]"), cs(";")]
     ],
    ["type-specifier", [ck("int"), s("DECLARE_TYPE"), ], [ck("void"),  s("DECLARE_TYPE"), ]],
    ["fun-declaration", [cs("("), s("FUNCTION"), s("SCOPE_START"), "params", cs(")"), "compound-stmt", s("SCOPE_END")]],
    ["params", [ck("void"), s("ADD_PARAM")], [ck("void"), s("DECLARE_TYPE"), s("ADD_PARAM"), "param-left", "param-list"], [ck("int"), s("DECLARE_TYPE"), s("ADD_PARAM"), "param-left", "param-list"]],
    ["param-list", [cs(","), "param", "param-list"], epsilon],
    ["param", ["type-specifier", s("ADD_PARAM"), "param-left"]],
    ["param-left", [Token(CTokenType.ID), s("DECLARE_NAME"), cs("["), cs("]")], [Token(CTokenType.ID), s("DECLARE_NAME")]],
    ["compound-stmt", [cs("{"), s("SCOPE_START"), "declaration-list", "statement-list", s("SCOPE_END"), cs("}")]],
    ["statement-list", ["statement-list", "statement"], epsilon],
    ["statement", ["expression-stmt", ], ["compound-stmt", ], ["selection-stmt", ], ["iteration-stmt", ],
     ["return-stmt", ], ["switch-stmt", ]],
    ["expression-stmt", ["expression", cs(";")], [ck("continue"), cs(";")], [ck("break"), cs(";")], [cs(";"), ]],
    ["selection-stmt", [ck("if"), cs("("), "expression", cs(")"), s("SCOPE_START"), "statement", s("SCOPE_END"),
                        ck("else"), s("SCOPE_START"), "statement", s("SCOPE_END")]],
    ["iteration-stmt", [ck("while"), cs("("), "expression", cs(")"), s("SCOPE_START"), "statement", s("SCOPE_END")]],
    ["return-stmt", [ck("return"), cs(";")], [ck("return"), "expression", cs(";")]],
    ["switch-stmt", [ck("switch"), cs("("), "expression", cs(")"), cs("{"), s("SCOPE_START  "), "case-stmts", "default-stmt", s("SCOPE_END"), cs("}")]],
    ["case-stmts", ["case-stmts", "case-stmt"], epsilon, ],
    ["case-stmt", [ck("case"), Token(CTokenType.NUM), cs(":"), "statement-list"]],
    ["default-stmt",
     [ck("default"), cs(":"), "statement-list"],
     epsilon
     ],
    ["expression",
     [Token(CTokenType.ID), "expression-left"],
     ["simple-expression"],
     ],
    ["expression-left",
     ["var-left", "expression-right"],
     ["call", "term-left", "additive-expression-left", "simple-expression-left"]
     ],
    ["expression-right",
     [cs("="),  "expression"],
     ["term-left", "additive-expression-left", "simple-expression-left"]
     ],
    ["var", [Token(CTokenType.ID), "var-left"]],
    ["var-left", [cs("["), "expression", cs("]")], epsilon],
    ["simple-expression", ["additive-expression-right", "simple-expression-left"]],
    ["simple-expression-left", ["relop", "additive-expression"], epsilon],
    ["relop",
     [cs("<")],
     [cs("==")],
     [cs(">")]
     ],
    ["additive-expression",
     ["term", "additive-expression-left"],
     ],
    ["additive-expression-left", ["addop", "term", "additive-expression-left"], epsilon],
    ["additive-expression-right",
     ["signed-factor-left", "term-left", "additive-expression-left"],
     ["factor-left", "term-left", "additive-expression-left"]
     ],
    ["addop",
     [cs("+")],
     [cs("-")],
     ],
    ["term", ["signed-factor", "term-left"]],
    ["term-left", [cs("*"), "signed-factor", "term-left"], epsilon],
    ["signed-factor",
     ["factor"],
     ["signed-factor-left"]
     ],
    ["signed-factor-left",
     [cs("+"), "factor"],
     [cs("-"), "factor"]
     ],
    ["factor",
     [Token(CTokenType.ID), "var-call"],
     ["factor-left"]
     ],
    ["factor-left",
     [cs("("), "expression", cs(")")],
     [Token(CTokenType.NUM)]
     ],
    ["var-call", ["var-left"], ["call"]],
    ["call", [cs("("), "args", cs(")")]],
    ["args",
     ["arg-list"],
     epsilon,
     ],
    ["arg-list",
     ["arg-list", cs(","), "expression"],
     ["expression"],
     ],
]
