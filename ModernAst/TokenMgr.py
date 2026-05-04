import tokenize
import io
import token
from objects import Token


"""
Менеджер токенов
Для перевода из генератора в массив
"""
class Manager:
    def __init__(self, source_code : str):
        self._source_code = source_code # исходный код 
        self._tokens = self.generate_tokens() # массив обьектов токенов

    @property
    def tokens_list(self):
        """
        Получение токенов через аттрибут
        Для инкапсуляции
        """

        return self._tokens

    def generate_tokens(self):
        """
        Преобразовение генератора в массив
        """

        buffer  = io.StringIO(self._source_code)
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
        """
        Вывод токенов в консоль
        """
        
        for i in self._tokens:
            print(i)