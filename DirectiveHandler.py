from ActionSymbol import ActionSymbol
from CodeGenerator import CodeGenerator
from SemanticSymbol import SemanticSymbol
from Semantics import Semantics


class DirectiveHandler:
    def __init__(self, semantics, code_generator):
        self.semantics = semantics
        self.code_generator = code_generator

    def handle_directive(self, directive, cur_non_terminal, cur_node):
        if isinstance(directive, SemanticSymbol):
            self.semantics.handle_semantic_symbol(directive, current_non_terminal=cur_non_terminal, current_node=cur_node)
        elif isinstance(directive, ActionSymbol):
            self.code_generator.handle_action_symbol(self.semantics, directive, current_non_terminal=cur_non_terminal, current_node=cur_node)