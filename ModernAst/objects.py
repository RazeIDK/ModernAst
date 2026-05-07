from dataclasses import dataclass, field
from typing import Tuple, Any
from enum import Enum, auto


# операторы
class Operator(Enum):
    # арифметические
    ADD = auto() # +
    SUB = auto() # -
    MUL = auto() # *
    DIV = auto() # /
    MOD = auto() # %
    POW = auto() # **
    FLOOR_DIV = auto() # //
    
    # сравнения
    EQ = auto() # ==
    NE = auto() # !=
    LT = auto() # <
    GT = auto() # >
    LE = auto() # <=
    GE = auto() # >=
    
    # логические
    AND = auto() # and
    OR = auto() # or
    NOT = auto() # not
    
    # битовые
    BIT_AND = auto() # &
    BIT_OR = auto() # |
    BIT_XOR = auto() # ^
    BIT_NOT = auto() # ~
    SHIFT_LEFT = auto() # <<
    SHIFT_RIGHT = auto() # >>
    
    def __str__(self):
        return {
            Operator.ADD: "+",
            Operator.SUB: "-",
            Operator.MUL: "*",
            Operator.DIV: "/",
            Operator.MOD: "%",
            Operator.POW: "**",
            Operator.FLOOR_DIV: "//",
            Operator.EQ: "==",
            Operator.NE: "!=",
            Operator.LT: "<",
            Operator.GT: ">",
            Operator.LE: "<=",
            Operator.GE: ">=",
            Operator.AND: "and",
            Operator.OR: "or",
            Operator.NOT: "not",
            Operator.BIT_AND: "&",
            Operator.BIT_OR: "|",
            Operator.BIT_XOR: "^",
            Operator.BIT_NOT: "~",
            Operator.SHIFT_LEFT: "<<",
            Operator.SHIFT_RIGHT: ">>",
        }.get(self, self.name.lower())
    
    @classmethod
    def get_all_symbols(cls) -> list:
        return (
            "+",
            "-",
            "*",
            "/",
            "%",
            "**",
            "//",
            "==",
            "!=",
            "<",
            ">",
            "<=",
            ">=",
            "and",
            "or",
            "not",
            "&",
            "|",
            "^",
            "~",
            "<<",
            ">>"
        )
    
    @classmethod
    def from_string(cls, symbol: str) -> "Operator":
        symbol_to_operator = {
            "+": cls.ADD,
            "-": cls.SUB,
            "*": cls.MUL,
            "/": cls.DIV,
            "%": cls.MOD,
            "**": cls.POW,
            "//": cls.FLOOR_DIV,
            "==": cls.EQ,
            "!=": cls.NE,
            "<": cls.LT,
            ">": cls.GT,
            "<=": cls.LE,
            ">=": cls.GE,
            "and": cls.AND,
            "or": cls.OR,
            "not": cls.NOT,
            "&": cls.BIT_AND,
            "|": cls.BIT_OR,
            "^": cls.BIT_XOR,
            "~": cls.BIT_NOT,
            "<<": cls.SHIFT_LEFT,
            ">>": cls.SHIFT_RIGHT,
        }
        
        if symbol not in symbol_to_operator:
            raise RuntimeError(f"Неизвестный оператор: {symbol}")
        
        return symbol_to_operator[symbol]


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

@dataclass
class Block:
    """
    Блок кода

    Поля:
        level: уровень вложенности (табы)
        tokens: токены в блоке
        parent: родительский блок
        children: вложенные блоки
    """
    level: int
    tokens: List[Any]
    parent: Optional["Block"] = None
    children: List["Block"] = None
    
    def __post_init__(self):
        self.children = []


# ноды
@dataclass(slots=True)
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
    value: Any

@dataclass(slots=True)
class BooleanLiteral(Literal):
    value: bool

@dataclass(slots=True)
class StringLiteral(Literal):
    value: str

@dataclass(slots=True)
class NumberLiteral(Literal):
    value: float | int


@dataclass(slots=True)
class Pass(Statement):
    pass


@dataclass(slots=True)
class Object(Expression):
    name : str

@dataclass(slots=True)
class Method(Object):
    pass

@dataclass(slots=True)
class Attribute(Object):
    pass

@dataclass
class Variable(Object):
    pass

@dataclass(slots=True)
class Call(Expression):
    objects : list[Object]
    args: list[Expression] = field(default_factory=list)


@dataclass(slots=True)
class Module(Object):
    pass

@dataclass(slots=True)
class Import(Statement):
    module : Module


@dataclass(slots=True)
class Function(Statement):
    """
    Обьект функции

    Поля:
        name: название функции
        body: тело функции
        args: аргументы функции
    """
    name: str
    body: list[Statement] = field(default_factory=list)
    args: list[Expression] = field(default_factory=list)


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
    body: list[Statement] = field(default_factory=list)
    elif_branches: list[tuple[Expression, list[Statement]]] = field(default_factory=list)
    else_body: Optional[list[Statement]] = None

@dataclass(slots=True)
class ElifConstruct(Statement):
    condition: Expression
    body: list[Statement] = field(default_factory=list)

@dataclass(slots=True)
class ElseConstruct(Statement):
    body: list[Statement] = field(default_factory=list)