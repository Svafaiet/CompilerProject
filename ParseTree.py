from DirectiveSymbol import DirectiveSymbol
from Production import epsilon


class ParseTree:
    def __init__(self):
        self.root = None
        self.stack = []

    def iterate(self, value):
        if len(self.stack) == 0:
            return
        top = self.stack.pop()
        top.iterate(value)
        if not top.is_finished():
            self.stack.append(top)
        else:
            self.iterate(top)

    def insert_rhs(self, rhs):
        self.stack.append(Node(rhs))
        if self.root is None:
            self.root = self.stack[0]

    def top_index(self):
        if not self.stack:
            return 0
        top = self.stack.pop()
        index = top.index
        self.stack.append(top)
        return index

    def view(self):
        return self.root.view("")


class Node:
    def __init__(self, rhs):
        self.rhs = rhs
        self.children = {}
        self.index = -1
        for i in range(len(rhs)):
            if not isinstance(rhs[i], DirectiveSymbol):
                self.children[i] = None
                if self.index == -1:
                    self.index = i

    def iterate(self, value):
        self.children[self.index] = value
        self.index += 1
        while self.index < len(self.rhs):
            if not isinstance(self.rhs[self.index], DirectiveSymbol):
                break
            self.index += 1

    def is_finished(self):
        return self.index == len(self.rhs)

    def view(self, prefix):
        ans = ""
        if self.rhs != epsilon:
            for i, value in list(
                    filter(lambda x: not isinstance(x[1], DirectiveSymbol), enumerate(self.rhs[:self.index]))):
                ans += prefix
                ans += "|- "
                ans += str(value)
                ans += "\n"
                if isinstance(value, str) and self.children[i] is not None:
                    ans += self.children[i].view(prefix + " ")
        else:
            ans = prefix + "|- EPSILON\n"
        return ans
