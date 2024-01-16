from .token import Token, TokenType
from .exc import LexerError


class Lexer:
    def __init__(self, source: str | None = None) -> None:
        self._source = source or ""
        self._tokens: list[Token] = []
        self._stop = len(self._source)
        self._current = 0
        self._start = 0

    def _lexeme(self) -> str:
        return self._source[self._start : self._current]

    def advance(self):
        self._current += 1

    def consume(self):
        self._start = self._current

    def add_token(self, type: TokenType):
        token = Token(type, self._lexeme(), self._start)
        self._tokens.append(token)

    def consume_token(self, type: TokenType):
        self.add_token(type)
        self.consume()

    def consume_char(self, type: TokenType | None = None):
        self.advance()
        if type is not None:
            self.consume_token(type)
        else:
            self.consume()

    def empty(self):
        return self._current >= self._stop

    def peek(self):
        return "" if self.empty() else self._source[self._current]

    reset = __init__

    def _scan(self):
        while not self.empty():
            match self.peek():
                case " ":
                    self.consume_char()
                case "*":
                    self.consume_char(TokenType.STAR)
                case "-":
                    self.consume_char(TokenType.MINUS)
                case "+":
                    self.consume_char(TokenType.PLUS)
                case "(":
                    self.consume_char(TokenType.LEFT)
                case ")":
                    self.consume_char(TokenType.RIGHT)
                case "^":
                    self.consume_char(TokenType.POWER)
                case "/":
                    self.consume_char(TokenType.SLASH)
                case ".":
                    self.consume_char(TokenType.DOT)
                case char:
                    if char.isdigit():
                        self.consume_number()
                    else:
                        raise LexerError(
                            f"Unexpected character: {char!r} in column {self._current}"
                        )

    def consume_number(self):
        while self.peek().isdigit():
            self.advance()
        self.consume_token(TokenType.NUMBER)

    def scan(self, src: str | None = None):
        self.reset(src)
        self._scan()
        eof = Token(TokenType.EOF, "", self._current)
        self._tokens.append(eof)
        return self._tokens
