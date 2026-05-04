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


# ноды
@dataclass(slots=True, frozen=True)
class Node:
    """
    Родительский класс узлов AST
    
    Поля:
        node_pos: Position
    """
    node_pos: Position


# имеет значение
@dataclass
class Expression(Node):
    pass

# выполняет
@dataclass
class Statement(Node):
    pass


@dataclass
class BinaryOp(Node):
    """
    Узел для бинарной операции

    Поля:
        left: левое значение
        operator: оператор
        right: правое значение

    Пример:
        BinaryOp(
            left=BooleanLiteral(value=True),
            operator="==",
            right=BooleanLiteral(value=True)
        )
    """
    left: Expression
    operator: str
    right: Expression


# литералы
@dataclass
class Literal(Expression):
    value : Any

@dataclass(slots=True)
class BooleanLiteral(Literal):
    value : bool

@dataclass(slots=True)
class StringLiteral(Literal):
    value : str

@dataclass(slots=True)
class NumberLiteral(Literal):
    value : float | int


# переменные
@dataclass
class Variable(Expression):
    name : str


@dataclass(slots=True)
class IfConstruct(Statement):
    """
    Конструкция условий (ветвления)

    Поля:
        condition: условие
        then_body: блок операторов для then
        elif_branches: список elif веток (каждая: условие, тело)
        else_body: блок операторов для else
    """
    condition: Expression
    then_body: List[Statement] = field(default_factory=list)
    elif_branches: List[tuple[Expression, List[Statement]]] = field(default_factory=list)
    else_body: Optional[List[Statement]] = None