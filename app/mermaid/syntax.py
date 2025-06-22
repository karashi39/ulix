from enum import StrEnum, Enum

_HEADER = "flowchart "

COMMENT_LITERAL = "%%"


class Header(StrEnum):
    LR = _HEADER + "LR"
    RL = _HEADER + "RL"
    TD = _HEADER + "TD"
    TB = _HEADER + "TB"
    BT = _HEADER + "BT"


class Arrow(StrEnum):
    LINK = "-->"
    DOT = "-.->"
    BOLD = "==>"


class Paren(Enum):
    PAREN = ("(", ")")
    BRACKET = ("[", "]")
