import tokenize
import io
import token
from objects import Token, Position


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

        # перебор генератора
        for t in generate_tokens:
            # позиция токена
            token_position = Position(t.start, t.end)
            
            # создание обьекта токенов
            token_object = Token(
                t.type,
                token.tok_name[t.type],
                t.string,
                token_position,
                t.line
            )
            
            # добавление в список обьектов токена
            token_objects.append(token_object)

        return token_objects

    def print_tokens(self):
        """
        Вывод токенов в консоль
        """

        for i in self._tokens:
            print(i)