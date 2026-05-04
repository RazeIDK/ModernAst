from objects import *
import keyword
from enum import Enum, auto


# контекст
class Context(Enum):
    NULL = auto()

    FUNCTION_CREATE = auto()
    FUNCTION_NAME = auto()



# строитель блоков
class BlockBuilder:
    def __init__(self, token_objects: List[Any]):
        self.tokens_objects = token_objects
    
    def build(self) -> Block:
        root = Block(level=0, tokens=[], parent=None)
        stack = [root]
        
        for token in self.tokens_objects:
            if token.t_name == "INDENT":
                new_block = Block(
                    level=len(stack),
                    tokens=[],
                    parent=stack[-1]
                )
                stack[-1].children.append(new_block)
                stack.append(new_block)
                
            elif token.t_name == "DEDENT":
                if len(stack) > 1:
                    stack.pop()
                    
            else:
                stack[-1].tokens.append(token)
        
        self._clean_tokens(root)
        self._remove_empty_blocks(root)
        
        return root
    
    def _clean_tokens(self, block):
        block.tokens = [t for t in block.tokens if t.t_name not in ("INDENT", "DEDENT")]
        for child in block.children:
            self._clean_tokens(child)
    
    def _remove_empty_blocks(self, block):
        """Удаляет пустые блоки"""
        for child in block.children[:]:
            self._remove_empty_blocks(child)
            if not child.tokens and not child.children:
                block.children.remove(child)


# Построение CFG
class ControlFlowGraph:
    def __init__(self, tokens_objects: list):
        self._tokens_objects = tokens_objects
        self._keywords = keyword.kwlist
        self._ast = []

        self.block_builder = BlockBuilder(self._tokens_objects)
        self.block = self.block_builder.build()

    def traverse(self):
        self._walk_block(self.block, level=0)
        print("ast:")
        print(self._ast)

    def _walk_block(self, block, level=0):
        if not hasattr(block, 'nodes'):
            block.nodes = self._parse_tokens(block.tokens)

        child_idx = 0
        children_list = [child for child in block.children if child.level == level + 1]

        for node in block.nodes:
            if hasattr(node, "body"):
                if child_idx < len(children_list):
                    child = children_list[child_idx]
                    self._walk_block(child, level + 1)
                    node.body = child.nodes
                    child_idx += 1
                else:
                    node.body = []

            if level == 0:
                self._ast.append(node)

    def _parse_tokens(self, tokens):
        count_tokens = len(tokens)
        context = Context.NULL
        stack = []
        local_ast = []
        i = 0

        while i < count_tokens:
            token_object = tokens[i]

            match token_object.t_name:
                case "NAME":
                    if token_object.t_string in self._keywords:
                        match token_object.t_string:
                            case "def":
                                stack.insert(0, token_object)
                                context = Context.FUNCTION_CREATE
                            case "pass":
                                pass_object = Pass(node_pos=token_object.t_pos)
                                local_ast.append(pass_object)
                    else:
                        match context:
                            case Context.FUNCTION_CREATE:
                                stack.insert(0, token_object)
                                context = Context.FUNCTION_NAME

                case "OP":
                    if context != Context.NULL:
                        match context:
                            case Context.FUNCTION_NAME:
                                start_pos = stack[1].t_pos.start
                                end_pos = token_object.t_pos.end
                                pos = Position(start_pos, end_pos)
                                name_function = stack[0].t_string

                                function_object = Function(
                                    node_pos=pos,
                                    name=name_function,
                                    args=[],
                                    body=[]
                                )
                                local_ast.append(function_object)
                                context = Context.NULL
                case _:
                    pass
            i += 1

        return local_ast