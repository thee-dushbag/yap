from . import nodes
from .typedef import Stringify


class PrintExpression(nodes.Visitor[str], Stringify[nodes.Expression]):
    def _binlr(self, expr: nodes.Binary) -> str:
        left = expr.left.accept(self)
        operator = expr.operator.lexeme
        right = expr.right.accept(self)
        return f"{left} {operator} {right}"

    def _binu(self, expr: nodes.Unary) -> str:
        operand = expr.operand.accept(self)
        operator = expr.operator.lexeme
        post = ")" if operator == "(" else ""
        if operator == "!":
            post = operator
            operator = ""
        return f"{operator}{operand}{post}"

    def accept_group(self, expr: nodes.Group) -> str:
        return self._binu(expr)

    def accept_uminus(self, expr: nodes.UMinus) -> str:
        return self._binu(expr)

    def accept_uplus(self, expr: nodes.UPlus) -> str:
        return self._binu(expr)

    def accept_unot(self, expr: nodes.UNot) -> str:
        return self._binu(expr)

    def accept_minus(self, expr: nodes.Minus) -> str:
        return self._binlr(expr)

    def accept_plus(self, expr: nodes.Plus) -> str:
        return self._binlr(expr)

    def accept_slash(self, expr: nodes.Slash) -> str:
        return self._binlr(expr)

    def accept_star(self, expr: nodes.Star) -> str:
        return self._binlr(expr)

    def accept_number(self, expr: nodes.Number) -> str:
        return expr.value.lexeme

    def accept_string(self, expr: nodes.String) -> str:
        return expr.value.lexeme

    def accept_ternary_cond(self, expr: nodes.TernaryCond) -> str:
        left = expr.left.accept(self)
        middle = expr.middle.accept(self)
        right = expr.right.accept(self)
        lop = expr.loperator.lexeme
        rop = expr.roperator.lexeme
        return f'{left} {lop} {middle} {rop} {right}'

    def tostr(self, thing: nodes.Expression) -> str:
        return thing.accept(self)
