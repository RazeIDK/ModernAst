from objects import *

class ControlFlowGraph:
    def __init__(self, tokens_objects : list):
        self.tokens_objects = tokens_objects

    def analyze(self):
        count_tokens_objects = len(self.tokens_objects)
        stack = []

        for i in range(count_tokens_objects - 1):
            token_object = self.tokens_objects[i]

            match token_object.t_name:
                case "OP":
                    if token_object.t_string in Operator.get_all_symbols():
                        print(Operator.from_string(token_object.t_string))