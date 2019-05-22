from Production import epsilon
from Token import CTokenType, Token


def ck(keyword_name):
    return Token(CTokenType.KEYWORD, keyword_name)


def cs(symbol_name):
    return Token(CTokenType.SYMBOL, symbol_name)


compressed_grammar = [
    ["program", ["declaration-list", Token(CTokenType.EOF)]],
    ["declaration-list", ["declaration-list", "declaration"], epsilon],
    ["declaration", ["type-specifier", "var-declaration", ], ["type-specifier", "fun-declaration", ]], #type-specifier added
    ["var-declaration",
     [Token(CTokenType.ID), cs(";")],
     [Token(CTokenType.ID), cs("["), Token(CTokenType.NUM), cs("]"), cs(";")]
     ],
    ["type-specifier", [ck("int"), ], [ck("void"), ]], #type-specifier removed
    ["fun-declaration", [Token(CTokenType.ID), cs("("), "params", cs(")"), "compound-stmt"]], #type-specifier removed
    ["params", [ck("void"), "param-name", "param-list"], [ck("int"), "param-name", "param-list"], [ck("void"), ]], #changed
    ["param-list", [cs(","), "param", "param-list"], epsilon], #changed
    ["param", ["type-specifier", "param-name"]], #changed
    ["param-name", [Token(CTokenType.ID)], [Token(CTokenType.ID), cs("["), cs("]")]], #added
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
     ["var", cs("="), "expression"],
     ["var", "simple-expression-var"], #changed
     ],
    ["var",
     [Token(CTokenType.ID)],
     [Token(CTokenType.ID), cs("["), "expression", cs("]")],
     ],
    ["simple-expression-var",
     ["additive-expression-var", "relop", "additive-expression"],
     ["additive-expression-var"],
     ],
    ["relop",
     [cs("<")],
     [cs("==")]
     ],
    ["additive-expression",
     ["additive-expression", "addop", "term"],
     ["term"],
     ],
    ["additive-expression-var",
     ["additive-expression-var", "addop", "term"],
     ["term-var"],
     ],
    ["addop",
     [cs("+")],
     [cs("-")],
     ],
    ["term",
     ["term", cs("*"), "signed-factor"],
     ["signed-factor"],
     ],
    ["term-var",
     ["term-var", cs("*"), "signed-factor"],
     ["signed-factor-var"],
     ],
    ["signed-factor",
     ["factor"],
     [cs("+"), "factor"],
     [cs("-"), "factor"],
     ],
    ["signed-factor-var",
     ["factor-var"],
     [cs("+"), "factor"],
     [cs("-"), "factor"],
     ],
    ["factor",
     [cs("("), "expression", cs(")")],
     ["var"],
     ["call"],
     [Token(CTokenType.NUM)],
     ],
    ["factor-var",
     [cs("("), "expression", cs(")")],
     epsilon,
     ["call"],
     [Token(CTokenType.NUM)],
     ],
    ["call", [Token(CTokenType.NUM), cs("("), "args", cs(")")]],
    ["args",
     ["arg-list"],
     epsilon,
     ],
    ["arg-list",
     ["arg-list", cs(","), "expression"],
     ["expression"],
     ],
]
