import typing as ty

if ty.TYPE_CHECKING:
    from .token import Token
else:
    Token = None


class Visitor(ty.Protocol):
    def accept_plus(self, expr: "Plus") -> ty.Any:
        ...

    def accept_minus(self, expr: "Minus") -> ty.Any:
        ...

    def accept_star(self, expr: "Star") -> ty.Any:
        ...

    def accept_power(self, expr: "Power") -> ty.Any:
        ...

    def accept_slash(self, expr: "Slash") -> ty.Any:
        ...

    def accept_group(self, expr: "Group") -> ty.Any:
        ...

    def accept_uplus(self, expr: "UPlus") -> ty.Any:
        ...

    def accept_uminus(self, expr: "UMinus") -> ty.Any:
        ...

    def accept_number(self, expr: "Number") -> ty.Any:
        ...


class Expression(ty.Protocol):
    def accept(self, visitor) -> ty.Any:
        ...

    def __eq__(self, other):
        ...


class Binary:
    def __init__(self, left: Expression, operator: Token, right: Expression) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def __eq__(self, expr):
        if isinstance(expr, Binary):
            return (
                self.left == expr.left
                and self.operator == expr.operator
                and self.right == expr.right
            )


class Unary:
    def __init__(self, operator: Token, right: Expression) -> None:
        self.operator = operator
        self.right = right

    def __eq__(self, expr):
        if isinstance(expr, Unary):
            return self.operator == expr.operator and self.right == expr.right


class Plus(Binary, Expression):
    def accept(self, visitor: Visitor):
        return visitor.accept_plus(self)


class Minus(Binary, Expression):
    def accept(self, visitor: Visitor):
        return visitor.accept_minus(self)


class Star(Binary, Expression):
    def accept(self, visitor: Visitor):
        return visitor.accept_star(self)


class Slash(Binary, Expression):
    def accept(self, visitor: Visitor):
        return visitor.accept_slash(self)


class Power(Binary, Expression):
    def accept(self, visitor: Visitor):
        return visitor.accept_power(self)


class Group(Unary, Expression):
    def accept(self, visitor: Visitor):
        return visitor.accept_group(self)


class UPlus(Unary, Expression):
    def accept(self, visitor: Visitor):
        return visitor.accept_uplus(self)


class UMinus(Unary, Expression):
    def accept(self, visitor: Visitor):
        return visitor.accept_uminus(self)


class Number(Expression):
    def __init__(self, token: Token) -> None:
        self.token = token

    def accept(self, visitor: Visitor):
        return visitor.accept_number(self)

    def __eq__(self, numb):
        if isinstance(numb, Number):
            return self.token == numb.token
