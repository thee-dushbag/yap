from .typedef import TokenStream, Location
from . import token
import typing as ty

__all__ = ("lex",)


def lex(source: str) -> TokenStream:
    yield from _Lexer_impl(source)._scan()


class _Lexer_impl:
    "Do not use this class directly, use function lex: `lex(source: str) -> TokenStream`"

    def __init__(self, source: str | None = None) -> None:
        self._source = source or ""
        self._stop: ty.Final[int] = len(self._source)
        self._current: int = 0
        self._column: int = 0
        self._start: int = 0
        self._line: int = 1

    def _peek(self) -> str:
        return "" if self._empty() else self._source[self._current]

    def _advance(self) -> str:
        consumed = self._peek()
        self._column += 1
        self._current += 1
        return consumed

    def _lexeme(self) -> str:
        return self._source[self._start : self._current]

    def _match(self, char: str):
        if self._peek() == char:
            return bool(self._advance())

    def _consume(self):
        consumed = self._lexeme()
        self._start = self._current
        return consumed

    def _make_token(
        self,
        tktype: token.TkType,
        location: Location | None = None,
        error: str | None = None,
    ) -> token.Token:
        location = self._capture_loc() if location is None else location
        lexeme = self._consume()
        if error is not None:
            lexeme = self._source.splitlines()[location.line - 1]
        return token.Token(tktype, lexeme, location, error)

    def _empty(self) -> bool:
        return self._current >= self._stop

    def _capture_loc(self) -> Location:
        return Location(self._line, self._column)

    def _consume_number(self) -> token.Token:
        location = self._capture_loc()
        while not self._empty() and self._peek().isdigit():
            self._advance()
        return self._make_token(token.TkType.NUMBER, location)

    def _advance_line(self):
        self._line += 1
        self._column = 0

    def _consume_string(self) -> token.Token:
        location = self._capture_loc()
        while True:
            char = self._advance()
            if char == '"': break
            elif char == "\n": self._advance_line()
            elif self._empty(): return self._error("Unterminated String.", location)
        return self._make_token(token.TkType.STRING, location)

    def _consume_identifier(self) -> token.Token:
        location = self._capture_loc()
        while not self._empty() and _isalnum(self._peek()):
            self._advance()
        tktype = token.keywords.get(self._lexeme(), token.TkType.IDENTIFIER)
        return self._make_token(tktype, location)

    def _consume_line_comment(self):
        while not self._empty() and self._peek() != '\n':
            self._advance()
    
    def _consume_multiline_comment(self):
        loc = self._capture_loc()
        while not self._empty():
            match self._advance():
                case '\n': self._advance_line()
                case '*': 
                    if self._advance() == '/': return
        return self._error("Unterminated multiline comment.", loc)

    def _error(self, message: str, location: Location | None = None):
        return self._make_token(token.TkType.ERROR, location, message)

    def _scan(self) -> TokenStream:
        t = token.TkType
        while not self._empty():
            match self._advance():
                case ("\n" | " " | "\t") as space:
                    if space == "\n": self._advance_line()
                    self._consume()
                case ".": yield self._make_token(t.DOT)
                case "*": yield self._make_token(t.STAR)
                case "#": yield self._make_token(t.HASH)
                case "+": yield self._make_token(t.PLUS)
                case "-": yield self._make_token(t.MINUS)
                case "?": yield self._make_token(t.QMARK)
                case ":": yield self._make_token(t.COLON)
                case ",": yield self._make_token(t.COMMA)
                case "$": yield self._make_token(t.DOLLAR)
                case "(": yield self._make_token(t.OPEN_PAREN)
                case "{": yield self._make_token(t.OPEN_BRACE)
                case ")": yield self._make_token(t.CLOSE_PAREN)
                case "}": yield self._make_token(t.CLOSE_BRACE)
                case '"': yield self._consume_string()
                case "/":
                    match self._peek():
                        case '/': self._consume_line_comment()
                        case '*':
                            self._advance() # Not part of end comment token
                            tk = self._consume_multiline_comment()
                            if tk is not None: yield tk
                        case _: yield self._make_token(t.SLASH)
                case "!":
                    token_type = t.BANG_EQUAL if self._match("=") else t.BANG
                    yield self._make_token(token_type)
                case ">":
                    token_type = t.GREATER_EQUAL if self._match("=") else t.GREATER
                    yield self._make_token(token_type)
                case "<":
                    token_type = t.LESS_EQUAL if self._match("=") else t.LESS
                    yield self._make_token(token_type)
                case "=":
                    token_type = t.EQUAL_EQUAL if self._match("=") else t.EQUAL
                    yield self._make_token(token_type)
                case unknown:
                    if unknown.isdigit(): yield self._consume_number()
                    elif _isalnum(unknown): yield self._consume_identifier()
                    else: yield self._error(f"Invalid character: {unknown!r}")


def _isalnum(char: str) -> bool:
    return char == "_" or char.isalnum()
