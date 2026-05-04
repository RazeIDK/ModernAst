import tokenize
import io
import token
from objects import Token


class Manager:
    def __init__(self, source_code : str):
        self.source_code = source_code
        self.tokens = self.generate_tokens()

    def generate_tokens(self):
        buffer  = io.StringIO(self.source_code)
        generate_tokens = tokenize.generate_tokens(buffer.readline)
        token_objects = []

        for t in generate_tokens:
            token_object = Token(
                t.type,
                token.tok_name[t.type],
                t.string,
                t.start,
                t.end,
                t.line
                )
            
            token_objects.append(token_object)

        return token_objects

    def print_tokens(self):
        for i in self.tokens:
            print(i)

    def _get_tokens(self):   
        return self.tokens
