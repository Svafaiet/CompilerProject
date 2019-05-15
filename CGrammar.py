from CToken import CTokenType, CToken
from Production import epsilon


def ck(keyword_name):
    return CToken(CTokenType.KEYWORD, keyword_name)


def cs(symbol_name):
    return CToken(CTokenType.SYMBOL, symbol_name)


compressed_grammar = [
    ["program", ["declaration-list", CToken(CTokenType.EOF)]],
    ["declaration-list", ["declaration-list", "declaration"], [epsilon, ]],
    ["declaration", ["var-declaration", ], ["fun-declaration", ]],
    ["var-declaration",
     ["type-specifier", CToken(CTokenType.ID), cs(";")],
     ["type-specifier", CToken(CTokenType.ID), cs("["), CToken(CTokenType.NUM), cs("]"), cs(";")]
     ],
    ["type-specifier", [ck("int"), ], [ck("void"), ]],
    ["fun-declaration", ["type-specifier", CToken(CTokenType.ID), cs("("), "params", cs(")"), "compound-stmt"]],
    ["params", ["param-list", ], [ck("void"), ]],
    ["param-list", ["param-list", cs("param")], ["param", ]],
    ["param", ["type-specifier", CToken(CTokenType.ID)],
     ["type-specifier", CToken(CTokenType.ID), cs("["), cs("]")]],
    ["compound-stmt", [cs("{"), "declaration-list", "statement-list", cs("}")]],
    ["statement-list", ["statement-list", "statement"], [epsilon, ]],
    ["statement", ["expression-stmt", ], ["compound-stmt", ], ["selection-stmt", ], ["iteration-stmt", ],
     ["return-stmt", ], ["switch-stmt", ]],
    ["expression-stmt", ["expression", cs(";")], [ck("continue"), cs(";")], [ck("break"), cs(";")], [cs(";"), ]],
    ["selection-stmt", [ck("if"), ], cs("("), "expression", cs(")"), "statement", ck("else"), "statement"],
    ["iteration-stmt", [ck("while"), cs("("), "expression", cs(")"), "statement"]],
    ["return-stmt", [ck("return"), cs(";")], [ck("return"), "expression", cs(";")]],
    ["switch-stmt", [ck("switch"), cs("("), "expression", cs(")"), cs("{"), "case-stmts", "default-stmt", cs("}")]],
    ["case-stmts", ["case-stmts", "case-stmt"], [epsilon, ]],
    ["case-stmt", ]  # todo
]
