from DirectiveSymbol import DirectiveSymbol
from Production import epsilon


class ParseTree:
    def __init__(self, root_none_terminal):
        self.root_none_terminal = root_none_terminal
        self.root = None
        self.stack = []

        # for code generation
        self.directive_handler = None

    def iterate(self, value):
        if len(self.stack) == 0:
            return
        top = self.stack.pop()
        top.iterate(value, self.directive_handler)
        if not top.is_finished():
            self.stack.append(top)
        else:
            self.iterate(top)

    def insert_rhs(self, rhs):
        top = self.top()
        new_node = None
        if None:
            new_node = Node(self.root_none_terminal, rhs, None)
        else:
            new_node = Node(top.rhs[top.index], rhs, top[top.index])
        self.stack.append(new_node)
        if self.root is None:
            self.root = self.stack[0]

    def top(self):
        if not self.stack:
            return None
        top = self.stack.pop()
        self.stack.append(top)
        return top

    def set_handler(self, directive_handler):
        self.directive_handler = directive_handler

    def view(self):
        return self.root.view("")


class Node:
    def __init__(self, none_terminal, rhs, last_node):
        self.none_terminal = none_terminal
        self.rhs = rhs
        self.children = {}
        self.index = -1
        self.last_node = last_node

    def pass_directives(self, directive_handler):
        for i in range(len(self.rhs)):
            if not isinstance(self.rhs[i], DirectiveSymbol):
                self.children[i] = None
                if self.index == -1:
                    self.index = i
            else:
                directive_handler.handle_directive(self.rhs[i], self.last_node)

    def iterate(self, value, directive_handler):
        self.children[self.index] = value
        self.index += 1
        while self.index < len(self.rhs):
            if not isinstance(self.rhs[self.index], DirectiveSymbol):
                break
            else:
                directive_handler.handle_directive(self.rhs[self.index], value)
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
