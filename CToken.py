import string

white_spaces = tuple(map(chr, [32, 10, 13, 9, 11, 12]))
digits = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
chars = tuple(string.ascii_lowercase) + tuple(string.ascii_uppercase)
symbols = ';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<'
keywords = "if", "else", "void", "while", "break", "continue", "switch", "default", "case", "return"


def make_keyword_states(str):
    keyword_list = []
    keyword_list.append((str, "KEYWORD"))
    for i in range(1, len(str)):
        keyword_list.append((str[:-i],))
    return keyword_list


def make_keyword_edges(str):
    keyword_edge_list = []
    keyword_edge_list.append((str[:-1], str, (str[-1],)))
    for i in range(2, len(str)):
        keyword_edge_list.append((str[:(-i)], str[:(-i + 1)], (str[-i],)))

    return keyword_edge_list


states = [
    ("start",),
    ("wrong",),
]
for kw_states in list(map(make_keyword_states, keywords)):
    states += kw_states

edges = [

]
for kw_edges in list(map(make_keyword_edges, keywords)):
    edges += kw_edges

print(tuple(states))
print(tuple(edges))
