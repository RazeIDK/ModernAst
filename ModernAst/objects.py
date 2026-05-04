from dataclasses import dataclass
from typing import Tuple

"""
Объект токена
Поля:
- Числовой индекс токена
- Строковое названи токена
- Строка
- Начало токена
- Конец токена
Параметры: slots для оптимизации
"""
@dataclass(slots=True)
class Token:
    t_type : int
    t_name : str
    t_string : str
    t_start : Tuple[int, int]
    t_end : Tuple[int, int]
    t_line : str

"""
Родительский класс узлов AST
Поля: начальное положение, конечное положение
Параметры: slots и frozen для оптимизации
"""
@dataclass(slots=True, frozen=True)
class Node:
    t_start : Tuple[int, int]
    t_end : Tuple[int, int]

@dataclass(slots=True, frozen=True)
class IfConstruct(Node):
    pass