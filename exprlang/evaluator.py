import typing as ty
from .nodes import (
    Expression,
    Visitor,
    Binary,
    Number,
    UMinus,
    Group,
    Power,
    Minus,
    Slash,
    UPlus,
    Star,
    Plus,
)


class Evaluator(Visitor):
    def accept_group(self, expr: Group):
        return expr.right.accept(self)

    def _binlr(self, expr: Binary) -> tuple[ty.Any, ty.Any]:
        left = expr.left.accept(self)
        right = expr.right.accept(self)
        return left, right

    def accept_minus(self, expr: Minus):
        left, right = self._binlr(expr)
        return left - right

    def accept_number(self, expr: Number) -> ty.Any:
        type = float if "." in expr.token.lexeme else int
        return type(expr.token.lexeme)

    def accept_plus(self, expr: Plus) -> ty.Any:
        left, right = self._binlr(expr)
        return left + right

    def accept_slash(self, expr: Slash) -> ty.Any:
        left, right = self._binlr(expr)
        if right == 0:
            raise ZeroDivisionError(
                f"Zero division error '{left} / 0' at column {expr.operator.column}"
            )
        return left / right

    def accept_power(self, expr: Power) -> ty.Any:
        left, right = self._binlr(expr)
        return left**right

    def accept_star(self, expr: Star) -> ty.Any:
        left, right = self._binlr(expr)
        return left * right

    def accept_uminus(self, expr: UMinus) -> ty.Any:
        right = expr.right.accept(self)
        return -right

    def accept_uplus(self, expr: UPlus) -> ty.Any:
        right = expr.right.accept(self)
        return +right

    def eval(self, root: Expression) -> ty.Any:
        return root.accept(self)
