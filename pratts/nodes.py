import typing as ty
from .typedef import _T_co

if ty.TYPE_CHECKING:
    from .token import Token
else:
    Token = object


class Visitor(ty.Protocol[_T_co]):
    def accept_number(self, expr: "Number") -> _T_co: ...
    def accept_string(self, expr: "String") -> _T_co: ...
    def accept_uminus(self, expr: "UMinus") -> _T_co: ...
    def accept_minus(self, expr: "Minus") -> _T_co: ...
    def accept_uplus(self, expr: "UPlus") -> _T_co: ...
    def accept_group(self, expr: "Group") -> _T_co: ...
    def accept_slash(self, expr: "Slash") -> _T_co: ...
    def accept_unot(self, expr: "UNot") -> _T_co: ...
    def accept_plus(self, expr: "Plus") -> _T_co: ...
    def accept_star(self, expr: "Star") -> _T_co: ...
    def accept_ternary_cond(self, expr: "TernaryCond") -> _T_co: ...


class Expression(ty.Protocol):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co: ...


class Binary:
    def __init__(self, left: Expression, operator: Token, right: Expression) -> None:
        self.left = left
        self.right = right
        self.operator = operator

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Binary) and (
            self.operator == other.operator
            and self.left == other.left
            and self.right == other.right
        ) or NotImplemented


class Ternary:
    def __init__(
        self,
        left: Expression,
        loperator: Token,
        middle: Expression,
        roperator: Token,
        right: Expression,
    ) -> None:
        self.left = left
        self.middle = middle
        self.right = right
        self.roperator = roperator
        self.loperator = loperator

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ternary) and (
            self.roperator == other.roperator
            and self.loperator == other.loperator
            and self.left == other.left
            and self.middle == other.middle
            and self.right == other.right
        ) or NotImplemented


class Unary:
    def __init__(self, operand: Expression, operator: Token) -> None:
        self.operand = operand
        self.operator = operator

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Unary) and (
            self.operator == other.operator
            and self.operand == other.operand
        ) or NotImplemented


class Literal:
    def __init__(self, value: Token) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Literal) and (
            self.value == other.value
        ) or NotImplemented


class Plus(Expression, Binary):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co:
        return visitor.accept_plus(self)


class Star(Expression, Binary):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co:
        return visitor.accept_star(self)


class Slash(Expression, Binary):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co:
        return visitor.accept_slash(self)


class Minus(Expression, Binary):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co:
        return visitor.accept_minus(self)


class UPlus(Expression, Unary):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co:
        return visitor.accept_uplus(self)


class UMinus(Expression, Unary):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co:
        return visitor.accept_uminus(self)


class UNot(Expression, Unary):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co:
        return visitor.accept_unot(self)


class Group(Expression, Unary):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co:
        return visitor.accept_group(self)


class Number(Expression, Literal):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co:
        return visitor.accept_number(self)


class String(Expression, Literal):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co:
        return visitor.accept_string(self)


class TernaryCond(Expression, Ternary):
    def accept(self, visitor: Visitor[_T_co]) -> _T_co:
        return visitor.accept_ternary_cond(self)
