import string
from enum import Enum
from functools import reduce
from DFA import white_spaces
from DFA import DFA

class TOKEN(Enum):
    NUM = "NUM"
    KEYWORD = "KEYWORD"
    ID = "ID"
    SYMBOL = "SYMBOL"
    COMMENT = "COMMENT"
    WHITE_SPACE = "WHITESPACE"
    EOF = "EOF"

digits = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
chars = tuple(string.ascii_lowercase) + tuple(string.ascii_uppercase)
symbols = ';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<'
# without '='
keywords = "if", "else", "void", "while", "break", "continue", "switch", "default", "case", "return"


def make_keyword_states(str):
    keyword_list = []
    keyword_list.append((str, TOKEN.KEYWORD))
    for i in range(1, len(str)):
        keyword_list.append((str[:-i],))
    return keyword_list


def make_keyword_edges(str):
    keyword_edge_list = []
    keyword_edge_list.append((str[:-1], str, (str[-1],)))
    for i in range(2, len(str)):
        keyword_edge_list.append((str[:(-i)], str[:(-i + 1)], (str[-i],)))
    keyword_edge_list.append(("start", str[0:1], str[0]))
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

    ("id", "id", digits + chars),

    ("start", "white_space", white_spaces),

    ("start", "eof", ('',)),

    ("start", "simple_symbol", symbols),
    ("start", "one_equation", ('=',)),
    ("one_equation", "dual_equation", ('=',)),

    ("cmnt", "cmnt_/", ('/',)),
    ("cmnt_/", "cmnt_//", ('/',)),
    ("cmnt_/", "cmnt_/*", ('*',)),
    ("cmnt_/*", "cmnt_/**", ('*',)),
    ("cmnt_/**", "cmnt", ('/',)),
    ("cmnt_//", "cmnt", ('\n',)),
]
kw_compressed_edges = reduce(lambda l1, l2: l1 + l2, list(map(make_keyword_edges, keywords)))
compressed_edges += kw_compressed_edges

remaining_characters = dict()
remaining_characters["start"] = list(chars)
for compressed_state in kw_compressed_states:
    if not (compressed_state[0] in remaining_characters) and (compressed_state[0] != "start"):
        remaining_characters[compressed_state[0]] = list(digits + chars)
for compressed_edge in kw_compressed_edges:
    for value in compressed_edge[2]:
        if not(value in remaining_characters[compressed_edge[0]]):
            remaining_characters[compressed_edge[0]].remove(value)

kw_to_id_edges = []
for compressed_state in kw_compressed_states:
    kw_to_id_edges.append((compressed_state[0], "id", remaining_characters[compressed_state[0]]))

compressed_edges += tuple(kw_to_id_edges)

dfa = DFA(compressed_states, compressed_edges)

print(tuple(compressed_states))
print(tuple(compressed_edges))
