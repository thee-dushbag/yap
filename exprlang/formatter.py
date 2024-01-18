from .nodes import (
    Expression,
    Visitor,
    Binary,
    Number,
    UMinus,
    Unary,
    Group,
    Power,
    Minus,
    Slash,
    UPlus,
    Star,
    Plus,
)


class Formatter(Visitor):
    def accept_number(self, expr: Number) -> str:
        return expr.token.lexeme

    def _lint_binary(self, expr: Binary) -> str:
        left: str = expr.left.accept(self)
        right: str = expr.right.accept(self)
        op: str = expr.operator.lexeme
        return f"{left} {op} {right}"

    def _lint_unary(self, expr: Unary) -> str:
        right: str = expr.right.accept(self)
        op: str = expr.operator.lexeme
        return f"{op}{right}"

    def accept_plus(self, expr: Plus) -> str:
        return self._lint_binary(expr)

    def accept_group(self, expr: Group) -> str:
        return "(" + expr.right.accept(self) + ")"

    def accept_minus(self, expr: Minus) -> str:
        return self._lint_binary(expr)

    def accept_power(self, expr: Power) -> str:
        return self._lint_binary(expr)

    def accept_slash(self, expr: Slash) -> str:
        return self._lint_binary(expr)

    def accept_star(self, expr: Star) -> str:
        return self._lint_binary(expr)

    def accept_uminus(self, expr: UMinus) -> str:
        return self._lint_unary(expr)

    def accept_uplus(self, expr: UPlus) -> str:
        return self._lint_unary(expr)

    def format(self, root: Expression) -> str:
        return root.accept(self)
