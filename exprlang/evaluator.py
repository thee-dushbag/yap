from . import nodes


class Evaluator(nodes.Visitor[float | int]):
    def accept_group(self, expr: nodes.Group):
        return expr.right.accept(self)

    def _binlr(self, expr: nodes.Binary):
        left = expr.left.accept(self)
        right = expr.right.accept(self)
        return left, right

    def accept_minus(self, expr: nodes.Minus):
        left, right = self._binlr(expr)
        return left - right

    def accept_number(self, expr: nodes.Number):
        type = float if "." in expr.token.lexeme else int
        return type(expr.token.lexeme)

    def accept_plus(self, expr: nodes.Plus):
        left, right = self._binlr(expr)
        return left + right

    def accept_slash(self, expr: nodes.Slash):
        left, right = self._binlr(expr)
        if right == 0:
            raise ZeroDivisionError(
                f"Zero division error '{left} / 0' at column {expr.operator.column}"
            )
        return left / right

    def accept_power(self, expr: nodes.Power):
        left, right = self._binlr(expr)
        return left**right

    def accept_star(self, expr: nodes.Star):
        left, right = self._binlr(expr)
        return left * right

    def accept_uminus(self, expr: nodes.UMinus):
        right = expr.right.accept(self)
        return -right

    def accept_uplus(self, expr: nodes.UPlus):
        right = expr.right.accept(self)
        return +right

    def eval(self, root: nodes.Expression):
        return root.accept(self)
