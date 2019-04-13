import string
from enum import Enum
from functools import reduce
from DFA import DFA
from LexicalAnalyzer import LexicalAnalyzer


class TOKEN(Enum):
    NUM = "NUM"
    KEYWORD = "KEYWORD"
    ID = "ID"
    SYMBOL = "SYMBOL"
    COMMENT = "COMMENT"
    WHITE_SPACE = "WHITESPACE"
    EOF = "EOF"


digits = '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
letters = tuple(string.ascii_lowercase) + tuple(string.ascii_uppercase)
symbols = ';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<'
# without '='
keywords = "if", "else", "void", "while", "break", "continue", "switch", "default", "case", "return"
# no keyword must contain other keywords
white_spaces = tuple(map(chr, [32, 10, 13, 9, 11, 12]))


def make_keyword_states(tok):
    keyword_list = [(tok, TOKEN.KEYWORD)]
    for i in range(1, len(tok)):
        keyword_list.append((tok[:-i], TOKEN.ID))
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
    ("num", TOKEN.NUM),
    ("id", TOKEN.ID),
    ("white_space", TOKEN.WHITE_SPACE),
    ("eof", TOKEN.EOF),
    ("simple_symbol", TOKEN.SYMBOL),
    ("one_equation", TOKEN.SYMBOL),
    ("dual_equation", TOKEN.SYMBOL),
    ("cmnt_/",),
    ("cmnt_/*", None, "cmnt_/*"),
    ("cmnt_/**", None, "cmnt_/*"),
    ("cmnt_//", None, "cmnt_//"),
    ("cmnt", TOKEN.COMMENT)
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

model = LexicalAnalyzer('test.txt', dfa)
token = model.get_next_token()
try:
    while True:
        print(next(token))
except StopIteration:
    pass
