from dataclasses import dataclass

@dataclass
class Token:
    t_type : int
    t_name : str
    t_string : str
    t_start : list
    t_end : list
    t_line : str

@dataclass
class Node:
    pass

