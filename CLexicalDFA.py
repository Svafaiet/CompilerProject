import string
from functools import reduce

from CToken import CTokenType
from DFA import DFA
from LexicalAnalyzer import LexicalAnalyzer

digits = '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
letters = tuple(string.ascii_lowercase) + tuple(string.ascii_uppercase)
symbols = ';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<'
# without '='
keywords = "if", "else", "void", "int", "while", "break", "continue", "switch", "default", "case", "return"
# no keyword must contain other keywords
white_spaces = tuple(map(chr, [32, 10, 13, 9, 11, 12]))


def make_keyword_states(tok):
    keyword_list = [(tok, CTokenType.KEYWORD)]
    for i in range(1, len(tok)):
        keyword_list.append((tok[:-i], CTokenType.ID))
    return keyword_list


def make_keyword_edges(tok):
    keyword_edge_list = [(tok[:-1], tok, (tok[-1],))]
    for i in range(2, len(tok)):
        keyword_edge_list.append((tok[:(-i)], tok[:(-i + 1)], (tok[-i],)))
    keyword_edge_list.append(("start", tok[0:1], tok[0]))
    return keyword_edge_list


# making compressed states
compressed_states = [
    ("start",),
    ("num", CTokenType.NUM),
    ("id", CTokenType.ID),
    ("white_space", CTokenType.WHITE_SPACE),
    ("eof", CTokenType.EOF),
    ("simple_symbol", CTokenType.SYMBOL),
    ("one_equation", CTokenType.SYMBOL),
    ("dual_equation", CTokenType.SYMBOL),
    ("cmnt_/",),
    ("cmnt_/*", None, "cmnt_/*"),
    ("cmnt_/**", None, "cmnt_/*"),
    ("cmnt_//", None, "cmnt_//"),
    ("cmnt", CTokenType.COMMENT)
]
kw_compressed_states = reduce(lambda l1, l2: l1 + l2, list(map(make_keyword_states, keywords)))
compressed_states += kw_compressed_states

# making compressed edges
compressed_edges = [
    ("start", "num", digits),
    ("num", "num", digits),

    ("id", "id", digits + letters),

    ("start", "white_space", white_spaces),

    ("start", "eof", ('',)),

    ("start", "simple_symbol", symbols),
    ("start", "one_equation", ('=',)),
    ("one_equation", "dual_equation", ('=',)),

    ("start", "cmnt_/", ('/',)),
    ("cmnt_/", "cmnt_//", ('/',)),
    ("cmnt_/", "cmnt_/*", ('*',)),
    ("cmnt_/*", "cmnt_/**", ('*',)),
    ("cmnt_/**", "cmnt", ('/',)),
    ("cmnt_//", "cmnt", ('\n',)),
    ("cmnt_//", "cmnt", ("",)),
]
kw_compressed_edges = reduce(lambda l1, l2: l1 + l2, list(map(make_keyword_edges, keywords)))
compressed_edges += kw_compressed_edges

remaining_characters = dict()
remaining_characters["start"] = list(letters)
for compressed_state in kw_compressed_states:
    if not (compressed_state[0] in remaining_characters) and (compressed_state[0] != "start"):
        remaining_characters[compressed_state[0]] = list(digits + letters)
for compressed_edge in kw_compressed_edges:
    for value in compressed_edge[2]:
        if value in remaining_characters[compressed_edge[0]]:
            remaining_characters[compressed_edge[0]].remove(value)

compressed_edges += [(item, 'id', tuple(remaining_characters[item])) for item in remaining_characters]

# print(tuple(compressed_states + [("start",)]))
# print(tuple(compressed_edges))
dfa = DFA.make_dfa(compressed_states, compressed_edges)
not_printing_tokens = [CTokenType.WHITE_SPACE, CTokenType.COMMENT, CTokenType.EOF]
model = LexicalAnalyzer('test.txt', dfa)
token = model.get_next_token()
with open('scanner.txt', mode='w') as output_file:
    with open("lexical_errors.txt", mode="w") as err_file:
        line = 1
        last_line = 1
        print_line = True
        first_error = True
        try:
            while True:
                lexeme, tok, error = next(token)
                if not error:
                    if lexeme == '\n' or (tok == CTokenType.COMMENT and '\n' in lexeme):
                        print_line = True
                        line += lexeme.count("\n")
                    if tok not in not_printing_tokens:
                        if print_line:
                            if line > 1:
                                output_file.write('\n')
                            output_file.write("{}. ".format(line))
                            print_line = False
                        output_file.write("({}, {}) ".format(tok.name, lexeme))
                else:
                    lexeme = lexeme.lstrip()
                    if last_line == line:
                        err_file.write("({}, invalid input) ".format(lexeme))
                    else:
                        if not first_error:
                            err_file.write("\n")
                        first_error = False
                        err_file.write("{}. ".format(line))
                        err_file.write("({}, invalid input) ".format(lexeme))
                    last_line = line
        except StopIteration:
            pass
