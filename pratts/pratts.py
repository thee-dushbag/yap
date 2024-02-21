import typing as ty, dataclasses as dt
from .typedef import ManagedStream
from . import nodes, token as tk
import enum

OExpr = ty.Optional[nodes.Expression]
ExprFN = ty.Callable[[ManagedStream, OExpr], OExpr]


class Prec(enum.IntEnum):
    NONE = enum.auto()
    TERNARY = enum.auto()
    SUBTRACT = enum.auto()
    ADD = enum.auto()
    MULTIPLY = enum.auto()
    DIVIDE = enum.auto()
    PRE_UNARY = enum.auto()
    POST_UNARY = enum.auto()
    PRIMARY = enum.auto()


def expression(stream: ManagedStream) -> nodes.Expression:
    return parse_prec(stream, Prec.TERNARY)


def expr_binary(stream: ManagedStream, left: OExpr):
    assert left is not None
    token = stream.peek()
    if token is None: return None
    props: tuple[type[nodes.Binary], Prec]
    match token.type:
        case tk.TkType.PLUS: props = nodes.Plus, Prec.ADD
        case tk.TkType.MINUS: props = nodes.Minus, Prec.SUBTRACT
        case tk.TkType.SLASH: props = nodes.Slash, Prec.DIVIDE
        case tk.TkType.STAR: props = nodes.Star, Prec.MULTIPLY
        case _: return
    eklass, prec = props
    next(stream) # Own the operator
    right = parse_prec(stream, prec)
    return eklass(left, token, right)


def expr_pre_unary(stream: ManagedStream, left: OExpr):
    token = stream.peek()
    if token is None: return
    eklass: type[nodes.Unary]
    match token.type:
        case tk.TkType.PLUS: eklass = nodes.UPlus
        case tk.TkType.MINUS: eklass = nodes.UMinus
        case tk.TkType.OPEN_PAREN:
            next(stream) # Own (
            operand = expression(stream)
            close_paren = next(stream, None)
            if close_paren is None or close_paren.type != tk.TkType.CLOSE_PAREN:
                raise Exception("Group expression was not closed.")
            return nodes.Group(operand, token)
        case _: return
    next(stream) # Own the operator +-
    operand = parse_prec(stream, Prec.PRE_UNARY)
    return eklass(operand, token)


def expr_ternary(stream: ManagedStream, left: OExpr):
    token = stream.peek()
    if token is None: return
    if left is None:
        raise Exception(f"MixFix operator missing left operand. {token}")
    props: tuple[type[nodes.Ternary], tk.TkType]
    match token.type:
        case tk.TkType.QMARK: props = nodes.TernaryCond, tk.TkType.COLON
        case _: return
    eklass, rop = props
    loperator = next(stream)
    middle = parse_prec(stream, Prec.TERNARY)
    token = stream.peek()
    if token is None or token.type != rop:
        raise Exception(f"Malformed mixfix expression, missing right operator {rop}")
    roperator = next(stream)
    right = parse_prec(stream, Prec.TERNARY)
    return eklass(left, loperator, middle, roperator, right)


def expr_post_unary(stream: ManagedStream, left: OExpr):
    token = stream.peek()
    if token is None: return
    if left is None:
        raise Exception(f"Post unary operator has no operand. {token}")
    match token.type:
        case tk.TkType.BANG: eklass = nodes.UNot
        case _: return
    next(stream) # Own the operator
    return eklass(left, token)


def expr_primary(stream: ManagedStream, left: OExpr):
    token = stream.peek()
    if token is None: return
    eklass: type[nodes.Literal]
    match token.type:
        case tk.TkType.NUMBER: eklass = nodes.Number
        case tk.TkType.STRING: eklass = nodes.String
        case _: return
    next(stream) # Own the value
    return eklass(token)


@dt.dataclass
class Rule:
    prefix: ExprFN | None
    infix: ExprFN | None
    prec: Prec


prec_table: ty.Final[dict[tk.TkType, Rule]] = {
    tk.TkType.OPEN_PAREN: Rule(expr_pre_unary, None, Prec.PRE_UNARY),
    tk.TkType.SLASH:      Rule(None, expr_binary, Prec.DIVIDE),
    tk.TkType.NUMBER:     Rule(expr_primary, None, Prec.PRIMARY),
    tk.TkType.STRING:     Rule(expr_primary, None, Prec.PRIMARY),
    tk.TkType.STAR:       Rule(None, expr_binary, Prec.MULTIPLY),
    tk.TkType.PLUS:       Rule(expr_pre_unary, expr_binary, Prec.ADD),
    tk.TkType.MINUS:      Rule(expr_pre_unary, expr_binary, Prec.SUBTRACT),
    tk.TkType.BANG:       Rule(None, expr_post_unary, Prec.POST_UNARY),
    tk.TkType.QMARK:      Rule(None, expr_ternary, Prec.TERNARY),
}


def get_rule(prec: tk.TkType) -> Rule:
    return prec_table.get(prec, Rule(None, None, Prec.NONE))


def parse_prec(stream: ManagedStream, prec: Prec) -> nodes.Expression:
    token = stream.peek()
    if token is None:
        raise Exception(f"Expected an expression, got {token}")
    rule = get_rule(token.type)
    if rule.prefix is not None:
        left = rule.prefix(stream, None) # Will consume the current token as theirs
        if left is None: raise Exception(f"Malformed expression table at {token}")
    else: raise Exception("Expected an expression.")
    while True:
        token = stream.peek()
        if token is None: break
        rule = get_rule(token.type)
        if prec > rule.prec: break
        if rule.infix is None: break
        left = rule.infix(stream, left) # Owns the current token
        if left is None:
            raise Exception("Left cannot be None")
    return left
