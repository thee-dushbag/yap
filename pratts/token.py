import enum, typing as ty
from .typedef import Location


class TkType(enum.StrEnum):
    DOT = enum.auto()  # .
    STAR = enum.auto()  # *
    PLUS = enum.auto()  # +
    HASH = enum.auto()  # #
    BANG = enum.auto()  # !
    LESS = enum.auto()  # <
    COMMA = enum.auto()  # ,
    SLASH = enum.auto()  # /
    MINUS = enum.auto()  # -
    QMARK = enum.auto()  # ?
    COLON = enum.auto()  # :
    EQUAL = enum.auto()  # =
    DOLLAR = enum.auto()  # $
    GREATER = enum.auto()  # >
    STRING = enum.auto()  # "[^"]*"
    NUMBER = enum.auto()  # [0-9]+
    DOUBLE_QUOTE = enum.auto()  # "
    OPEN_PAREN = enum.auto()  # (
    OPEN_BRACE = enum.auto()  # }
    CLOSE_PAREN = enum.auto()  # )
    CLOSE_BRACE = enum.auto()  # {
    BANG_EQUAL = enum.auto()  # !=
    LESS_EQUAL = enum.auto()  # <=
    EQUAL_EQUAL = enum.auto()  # ==
    GREATER_EQUAL = enum.auto()  # >=
    IDENTIFIER = enum.auto()  # [a-zA-Z_]+
    ERROR = enum.auto()  # LexingErrorToken


class Token:
    def __init__(
        self,
        tktype: TkType,
        lexeme: str,
        location: Location,
        error: str | None = None,
    ) -> None:
        self.type = tktype
        self.error = error
        self.lexeme = lexeme
        self.location = location

    @property
    def is_error(self) -> bool:
        return self.error is not None

    @property
    def line(self) -> int:
        return self.location.line

    @property
    def column(self) -> int:
        return self.location.column

    def __len__(self) -> int:
        return len(self.lexeme)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Token) and (
            self.lexeme == other.lexeme
            and self.type == other.type
        ) or NotImplemented

    def __str__(self) -> str:
        return f"Token({self.type!s}, {self.lexeme!r}, {self.line}:{self.column})"

    def __repr__(self) -> str:
        return (
            f"Token(type={self.type!s}, lexeme={self.lexeme!r}, "
            f"line={self.line}, column={self.column}, id={hex(id(self))})"
        )


keywords: ty.Final[dict[str, TkType]] = {}
