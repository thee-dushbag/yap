import typing as ty

if ty.TYPE_CHECKING:
    from .token import Token
else:
    Token = None


class BaseError(Exception): ...


class Error(BaseError): ...


class LexError(Error):
    def __init__(self, error_token: Token) -> None:
        self._msg = str(error_token.error)
        self._line = error_token.line
        self._column = error_token.column
        self._src = error_token.lexeme
        self._len = len(error_token)

    def __str__(self) -> str:
        l = "------------------------"
        s1 = f'\033[94;1m{self._line}\033[0m {self._src}'
        s2 = " " * (self._column + len(str(self._line))) + "\033[91;1m^\033[0m"
        s3 = f"[line: {self._line} column: {self._column}]: {self._msg}"
        return '\n'.join([s3, l, s1, s2, l])

    __repr__ = __str__
