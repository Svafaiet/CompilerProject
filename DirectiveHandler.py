from ActionSymbol import ActionSymbol
from CodeGenerator import CodeGenerator
from SemanticSymbol import SemanticSymbol
from Semantics import Semantics


class DirectiveHandler:
    def __init__(self, error_writer, file_out):
        self.semantics = Semantics(error_writer=error_writer)
        self.code_generator = CodeGenerator(self.semantics, file_out=file_out)

    def handle_directive(self, directive, cur_non_terminal, cur_node):
        if isinstance(directive, SemanticSymbol):
            self.semantics.handle_semantic_symbol(directive, current_non_terminal=cur_non_terminal,
                                                  current_node=cur_node)
        elif isinstance(directive, ActionSymbol):
            pass
            # self.code_generator.handle_action_symbol(directive, current_non_terminal=cur_non_terminal,
            #                                          current_node=cur_node)
