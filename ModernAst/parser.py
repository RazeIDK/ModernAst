from objects import *
import keyword
from enum import Enum, auto


# контекст
class Context(Enum):
    NULL = auto()

    FUNCTION_CREATE = auto()
    FUNCTION_NAME = auto()



# Строитель блоков
class BlockBuilder:
    def __init__(self, token_objects: List[Any]):
        self.tokens_objects = token_objects
        self.blocks = []
        self.current_block = None
        self.stack = []
    
    def build(self) -> List[Block]:
        count_tokens_objects = len(self.tokens_objects)

        current_block = Block(level=0, tokens=[])
        self.stack = [current_block]
        
        for i in range(count_tokens_objects - 1):
            token = self.tokens_objects[i]
            
            if token.t_name == "INDENT":
                new_block = Block(
                    level=len(self.stack),
                    tokens=[],
                    parent=self.stack[-1]
                )
                self.stack[-1].children.append(new_block)
                self.stack.append(new_block)
            elif token.t_name == "DEDENT":
                if len(self.stack) > 1:
                    self.stack.pop()
            else:
                self.stack[-1].tokens.append(token)
        
        return self.stack[0]


# Построение CFG
class ControlFlowGraph:
    def __init__(self, tokens_objects : list):
        self._tokens_objects = tokens_objects
        self._keywords = keyword.kwlist
        self._ast = []

        self.block_builder = BlockBuilder(self._tokens_objects)
        self.blocks = self.block_builder.build()

    def analyze(self):
        count_tokens_objects = len(self._tokens_objects)
        context = Context.NULL
        stack = []

        print(self.blocks)

        for i in range(count_tokens_objects - 1):
            token_object = self._tokens_objects[i]

            match token_object.t_name:
                case "NAME":
                    if token_object.t_string in self._keywords:
                        match token_object.t_string:
                            case "def":
                                stack.insert(0, token_object)
                                context = Context.FUNCTION_CREATE
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

                                function_object = Function(pos, name_function)
                                self._ast.append(function_object)

                                context = Context.NULL
                    else:
                        pass
        print(self._ast)