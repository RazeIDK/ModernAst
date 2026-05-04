from objects import *
import keyword


"""
Построение CFG
"""
class ControlFlowGraph:
    def __init__(self, tokens_objects : list):
        self._tokens_objects = tokens_objects
        self._keywords = keyword.kwlist
        self._ast = []

    def build_blocks(self):
        pass

    def analyze(self):
        count_tokens_objects = len(self._tokens_objects)

        for i in range(count_tokens_objects - 1):
            token_object = self._tokens_objects[i]

            match token_object.t_name:
                case "NAME":
                    if token_object.t_string in self._keywords:
                        match token_object.t_string:
                            case "def":
                                pass
                    else:
                        pass