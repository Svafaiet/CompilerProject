from Production import epsilon
from Token import CTokenType, Token


def ck(keyword_name):
    return Token(CTokenType.KEYWORD, keyword_name)


def cs(symbol_name):
    return Token(CTokenType.SYMBOL, symbol_name)


compressed_grammar = [
    ["program", ["declaration-list", Token(CTokenType.EOF)]],
    ["declaration-list", ["declaration-list", "declaration"], epsilon],
    ["declaration", ["type-specifier", Token(CTokenType.ID), "var-func-declaration", ]],
    ["var-func-declaration", ["var-declaration"], ["fun-declaration"]],
    ["var-declaration",
     [cs(";")],
     [cs("["), Token(CTokenType.NUM), cs("]"), cs(";")]
     ],
    ["type-specifier", [ck("int"), ], [ck("void"), ]],
    ["fun-declaration", [cs("("), "params", cs(")"), "compound-stmt"]],
    ["params", [ck("void")], [ck("void"), "param-left", "param-list"], [ck("int"), "param-left", "param-list"]],
    ["param-list", [cs(","), "param", "param-list"], epsilon],
    ["param", ["type-specifier", "param-left"]],
    ["param-left", [Token(CTokenType.ID), cs("["), cs("]")], [Token(CTokenType.ID)]],
    ["compound-stmt", [cs("{"), "declaration-list", "statement-list", cs("}")]],
    ["statement-list", ["statement-list", "statement"], epsilon],
    ["statement", ["expression-stmt", ], ["compound-stmt", ], ["selection-stmt", ], ["iteration-stmt", ],
     ["return-stmt", ], ["switch-stmt", ]],
    ["expression-stmt", ["expression", cs(";")], [ck("continue"), cs(";")], [ck("break"), cs(";")], [cs(";"), ]],
    ["selection-stmt", [ck("if"), cs("("), "expression", cs(")"), "statement", ck("else"), "statement"]],
    ["iteration-stmt", [ck("while"), cs("("), "expression", cs(")"), "statement"]],
    ["return-stmt", [ck("return"), cs(";")], [ck("return"), "expression", cs(";")]],
    ["switch-stmt", [ck("switch"), cs("("), "expression", cs(")"), cs("{"), "case-stmts", "default-stmt", cs("}")]],
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
     [cs("="), "expression"],
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
