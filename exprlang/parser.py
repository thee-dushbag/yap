from .token import Token, TokenType
from .exc import ParserError
from . import nodes


class Parser:
    def __init__(self, tokens: list[Token] | None = None) -> None:
        self._tokens = tokens or []
        self._current = 0

    def peek(self) -> Token:
        return self._tokens[self._current]

    def peektype(self) -> TokenType:
        return self.peek().type

    def expression(self) -> nodes.Expression:
        return self.minus()

    def minus(self):
        left = self.plus()
        while self.peektype() == TokenType.MINUS:
            operator = self.advance()
            left = nodes.Minus(left, operator, self.plus())
        return left

    def plus(self):
        left = self.star()
        while self.peektype() == TokenType.PLUS:
            operator = self.advance()
            left = nodes.Plus(left, operator, self.star())
        return left

    def star(self):
        left = self.slash()
        while self.peektype() == TokenType.STAR:
            operator = self.advance()
            left = nodes.Star(left, operator, self.slash())
        return left

    def slash(self):
        left = self.unary()
        while self.peektype() == TokenType.SLASH:
            operator = self.advance()
            left = nodes.Slash(left, operator, self.unary())
        return left

    def unary(self):
        if self.peektype() in (TokenType.PLUS, TokenType.MINUS):
            operator = self.advance()
            right = self.unary()
            if operator.type == TokenType.PLUS:
                return nodes.UPlus(operator, right)
            return nodes.UMinus(operator, right)
        return self.power()

    def power(self):
        left = self.group()
        while self.peektype() == TokenType.POWER:
            operator = self.advance()
            left = nodes.Power(left, operator, self.group())
        return left

    def group(self):
        if self.peektype() == TokenType.LEFT:
            operator = self.advance()
            middle = self.expression()
            self.consume(
                TokenType.RIGHT,
                f"Group expression was never closed at column {operator.column}",
            )
            return nodes.Group(operator, middle)
        return self.number()

    def number(self):
        token = self.consume(TokenType.NUMBER, f"Expected a number, got {self.peek()}")
        if self.peektype() == TokenType.DOT:
            token.lexeme += self.advance().lexeme
            token.lexeme += self.consume(
                TokenType.NUMBER, f"Expected a number after the dot at {token.column}"
            ).lexeme
        return nodes.Number(token)

    reset = __init__

    def empty(self):
        return self.peektype() == TokenType.EOF

    def advance(self):
        consumed = self.peek()
        self._current += 1
        return consumed

    def consume(self, type: TokenType, message: str):
        if self.empty() or self.peektype() != type:
            raise ParserError(message)
        return self.advance()

    def parse(self, tokens: list[Token] | None = None):
        self.reset(tokens)
        return self.expression()
