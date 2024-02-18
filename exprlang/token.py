import enum


class TokenType(enum.StrEnum):
    NUMBER = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()
    SLASH = enum.auto()
    MINUS = enum.auto()
    STAR = enum.auto()
    PLUS = enum.auto()
    POWER = enum.auto()
    EOF = enum.auto()
    DOT = enum.auto()


class Token:
    def __init__(self, type: TokenType, lexeme: str, column: int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.column = column

    def __str__(self) -> str:
        return f"Token({self.type!s}, {self.lexeme!r}, {self.column})"

    __repr__ = __str__

    def __eq__(self, token: object):
        if isinstance(token, Token):
            return (
                self.type == token.type
                and self.lexeme == token.lexeme
                and self.column == token.column
            )
        return NotImplemented
