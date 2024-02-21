from math import factorial
from . import nodes
import typing as ty


class Interpreter(nodes.Visitor[float | int]):
    def _binlr(self, expr: nodes.Binary) -> tuple[float, float]:
        left = expr.left.accept(self)
        right = expr.right.accept(self)
        return left, right

    def accept_minus(self, expr: nodes.Minus) -> float | int:
        left, right = self._binlr(expr)
        return left - right

    def accept_plus(self, expr: nodes.Plus) -> float | int:
        left, right = self._binlr(expr)
        return left + right

    def accept_slash(self, expr: nodes.Slash) -> float | int:
        left, right = self._binlr(expr)
        return left / right

    def accept_star(self, expr: nodes.Star) -> float | int:
        left, right = self._binlr(expr)
        return left * right

    def accept_uplus(self, expr: nodes.UPlus) -> float | int:
        return +expr.operand.accept(self)

    def accept_uminus(self, expr: nodes.UMinus) -> float | int:
        return -expr.operand.accept(self)

    def accept_group(self, expr: nodes.Group) -> float | int:
        return expr.operand.accept(self)

    def accept_string(self, expr: nodes.String) -> float | int:
        return ty.cast(float, expr.value.lexeme[1:-1])

    def accept_number(self, expr: nodes.Number) -> float | int:
        type = float if "." in expr.value.lexeme else int
        return type(expr.value.lexeme)

    def accept_unot(self, expr: nodes.UNot) -> float | int:
        return factorial(int(expr.operand.accept(self)))

    def accept_ternary_cond(self, expr: nodes.TernaryCond) -> float | int:
        cond = expr.left.accept(self)
        return expr.middle.accept(self) if cond else expr.right.accept(self)

    def eval(self, expr: nodes.Expression) -> float | int:
        return expr.accept(self)
