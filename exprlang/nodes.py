import typing as ty

if ty.TYPE_CHECKING:
    from .token import Token
else:
    Token = None

_T_co = ty.TypeVar("_T_co", covariant=True)


class Visitor(ty.Protocol[_T_co]):
    def accept_plus(self, expr: "Plus") -> _T_co: ...

    def accept_minus(self, expr: "Minus") -> _T_co: ...

    def accept_star(self, expr: "Star") -> _T_co: ...

    def accept_power(self, expr: "Power") -> _T_co: ...

    def accept_slash(self, expr: "Slash") -> _T_co: ...

    def accept_group(self, expr: "Group") -> _T_co: ...

    def accept_uplus(self, expr: "UPlus") -> _T_co: ...

    def accept_uminus(self, expr: "UMinus") -> _T_co: ...

    def accept_number(self, expr: "Number") -> _T_co: ...


class Expression(ty.Protocol):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co: ...

    def __eq__(self, other: object) -> bool: ...


class Binary:
    def __init__(self, left: Expression, operator: Token, right: Expression) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def __eq__(self, expr: object) -> bool:
        return isinstance(expr, Binary) and (
            self.left == expr.left
            and self.operator == expr.operator
            and self.right == expr.right
        ) or NotImplemented


class Unary:
    def __init__(self, operator: Token, right: Expression) -> None:
        self.operator = operator
        self.right = right

    def __eq__(self, expr: object) -> bool:
        return isinstance(expr, Unary) and (
            self.operator == expr.operator
            and self.right == expr.right
        ) or NotImplemented


class Plus(Binary, Expression):
    def accept(self, visitor: Visitor[_T_co]):
        return visitor.accept_plus(self)


class Minus(Binary, Expression):
    def accept(self, visitor: Visitor[_T_co]):
        return visitor.accept_minus(self)


class Star(Binary, Expression):
    def accept(self, visitor: Visitor[_T_co]):
        return visitor.accept_star(self)


class Slash(Binary, Expression):
    def accept(self, visitor: Visitor[_T_co]):
        return visitor.accept_slash(self)


class Power(Binary, Expression):
    def accept(self, visitor: Visitor[_T_co]):
        return visitor.accept_power(self)


class Group(Unary, Expression):
    def accept(self, visitor: Visitor[_T_co]):
        return visitor.accept_group(self)


class UPlus(Unary, Expression):
    def accept(self, visitor: Visitor[_T_co]):
        return visitor.accept_uplus(self)


class UMinus(Unary, Expression):
    def accept(self, visitor: Visitor[_T_co]):
        return visitor.accept_uminus(self)


class Number(Expression):
    def __init__(self, token: Token) -> None:
        self.token = token

    def accept(self, visitor: Visitor[_T_co]):
        return visitor.accept_number(self)

    def __eq__(self, numb: object) -> bool:
        return isinstance(numb, Number) and self.token == numb.token or NotImplemented
