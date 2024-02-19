from . import nodes


class Formatter(nodes.Visitor[str]):
    def accept_number(self, expr: nodes.Number):
        return expr.token.lexeme

    def _lint_binary(self, expr: nodes.Binary):
        left: str = expr.left.accept(self)
        right: str = expr.right.accept(self)
        op: str = expr.operator.lexeme
        return f"{left} {op} {right}"

    def _lint_unary(self, expr: nodes.Unary):
        right: str = expr.right.accept(self)
        op: str = expr.operator.lexeme
        return f"{op}{right}"

    def accept_plus(self, expr: nodes.Plus):
        return self._lint_binary(expr)

    def accept_group(self, expr: nodes.Group):
        return "(" + expr.right.accept(self) + ")"

    def accept_minus(self, expr: nodes.Minus):
        return self._lint_binary(expr)

    def accept_power(self, expr: nodes.Power):
        return self._lint_binary(expr)

    def accept_slash(self, expr: nodes.Slash):
        return self._lint_binary(expr)

    def accept_star(self, expr: nodes.Star):
        return self._lint_binary(expr)

    def accept_uminus(self, expr: nodes.UMinus):
        return self._lint_unary(expr)

    def accept_uplus(self, expr: nodes.UPlus):
        return self._lint_unary(expr)

    def format(self, root: nodes.Expression):
        return root.accept(self)
