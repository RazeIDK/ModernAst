from dataclasses import dataclass
from typing import Tuple, Any


# токены
@dataclass
class Position():
    """
    Класс позиции

    Поля:
        start: начало позиции
        end: конец позиции

    Пример:
        Position(start=(1, 0), end=(1, 4)) # с 1 строки (1 символ) по 1 строку (4 символ)
    """
    start: Tuple[int, int]
    end: Tuple[int, int]


@dataclass(slots=True)
class Token:
    """
    Объект токена
    
    Поля:
        t_type: числовой индекс типа токена
        t_name: название типа токена
        t_string: строка токена
        t_pos: позиция токена
        t_line: полная строка токена
    
    Пример:
        Token(
            t_type=4,
            t_name='NEWLINE',
            t_string='\n',
            t_pos=Position(
                start=(3, 13),
                end=(3, 14)
                ),
            t_line='    print(dd)\n'
            )
    """
    t_type: int
    t_name: str
    t_string: str
    t_pos: Position
    t_line: str


# литералы
@dataclass
class Literal:
    value : Any

@dataclass(slots=True)
class BooleanLiteral(Literal):
    value : bool

@dataclass(slots=True)
class StringLiteral(Literal):
    value : string

@dataclass(slots=True)
class NumberLiteral(Literal):
    value : float | int


# переменные
@dataclass
class Variable:
    pass # заглушка


# ноды
@dataclass(slots=True, frozen=True)
class Node:
    """
    Родительский класс узлов AST
    
    Поля:
        node_pos: Position
    """
    node_pos: Position


@dataclass(slots=True, frozen=True)
class IfConstruct(Node):
    nodes : list[Node]