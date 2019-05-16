from Production import epsilon
from Token import CTokenType, Token


def ck(keyword_name):
    return Token(CTokenType.KEYWORD, keyword_name)


def cs(symbol_name):
    return Token(CTokenType.SYMBOL, symbol_name)


compressed_grammar = [
    ["program", ["declaration-list", Token(CTokenType.EOF)]],
    ["declaration-list", ["declaration-list", "declaration"], [epsilon]],
    ["declaration", ["var-declaration", ], ["fun-declaration", ]],
    ["var-declaration",
     ["type-specifier", Token(CTokenType.ID), cs(";")],
     ["type-specifier", Token(CTokenType.ID), cs("["), Token(CTokenType.NUM), cs("]"), cs(";")]
     ],
    ["type-specifier", [ck("int"), ], [ck("void"), ]],
    ["fun-declaration", ["type-specifier", Token(CTokenType.ID), cs("("), "params", cs(")"), "compound-stmt"]],
    ["params", ["param-list", ], [ck("void"), ]],
    ["param-list", ["param-list", cs("param")], ["param", ]],
    ["param", ["type-specifier", Token(CTokenType.ID)],
     ["type-specifier", Token(CTokenType.ID), cs("["), cs("]")]],
    ["compound-stmt", [cs("{"), "declaration-list", "statement-list", cs("}")]],
    ["statement-list", ["statement-list", "statement"], [epsilon]],
    ["statement", ["expression-stmt", ], ["compound-stmt", ], ["selection-stmt", ], ["iteration-stmt", ],
     ["return-stmt", ], ["switch-stmt", ]],
    ["expression-stmt", ["expression", cs(";")], [ck("continue"), cs(";")], [ck("break"), cs(";")], [cs(";"), ]],
    ["selection-stmt", [ck("if"), cs("("), "expression", cs(")"), "statement", ck("else"), "statement"]],
    ["iteration-stmt", [ck("while"), cs("("), "expression", cs(")"), "statement"]],
    ["return-stmt", [ck("return"), cs(";")], [ck("return"), "expression", cs(";")]],
    ["switch-stmt", [ck("switch"), cs("("), "expression", cs(")"), cs("{"), "case-stmts", "default-stmt", cs("}")]],
    ["case-stmts", ["case-stmts", "case-stmt"], [epsilon, ]],
    ["case-stmt", ["case", Token(CTokenType.NUM), cs(":"), "statement-list"]],
    ["default-stmt",
     [ck("default"), cs(":"), "statement-list"],
     [epsilon]
     ],
    ["expression",
     ["var", cs("="), "expression"],
     ["simple-expression"],
     ],
    ["var",
     [Token(CTokenType.ID)],
     [Token(CTokenType.ID), cs("["), "expression", cs("]")],
     ],
    ["simple-expression",
     ["additive-expression", "relop", "additive-expression"],
     ["additive-expression"],
     ],
    ["relop",
     [cs("<")],
     [cs("==")]
     ],
    ["additive-expression",
     ["additive-expression", "addop", "term"],
     ["term"],
     ],
    ["addop",
     [cs("+")],
     [cs("-")],
     ],
    ["term",
     ["term", cs("*"), "signed-factor"],
     ["signed-factor"],
     ],
    ["signed-factor",
     ["factor"],
     [cs("+"), "factor"],
     [cs("-"), "factor"],
     ],
    ["factor",
     [cs("("), "expression", cs(")")],
     ["var"],
     ["call"],
     [Token(CTokenType.NUM)],
     ],
    ["call", [Token(CTokenType.NUM), cs("("), "args", cs(")")]],
    ["args",
     ["arg-list"],
     [epsilon],
     ],
    ["arg-list",
     ["arg-list", cs(","), "expression"],
     ["expression"],
     ],
]
