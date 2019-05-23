from Directive import Directive
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
        if self.root == None:
            self.root = self.stack[0]

    def view(self):
        return self.root.view("")


class Node:
    def __init__(self, rhs):
        self.rhs = rhs
        self.children = {}
        self.index = 0
        for i in range(len(rhs)):
            if not isinstance(rhs[i], Directive):
                self.children[i] = None

    def iterate(self, value):
        self.children[self.index] = value
        while self.index < len(self.rhs):
            if not isinstance(self.rhs[self.index], Directive):
                break
            self.index += 1

    def is_finished(self):
        return self.index == len(self.rhs)

    def view(self, prefix):
        ans = ""
        if self.rhs != epsilon:
            for i, value in list(filter(lambda x: not isinstance(x[1], Directive) ,enumerate(self.rhs[:self.index]))):
                ans += prefix
                ans += str(value)
                ans += "\n"
                if isinstance(value, str):
                    ans += self.rhs[i].view(prefix + "\t")
        return ans
