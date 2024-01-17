from .instructions import Instruction
from .nodes import (
    Expression,
    Visitor,
    Number,
    UMinus,
    Group,
    Slash,
    Power,
    UPlus,
    Minus,
    Plus,
    Star,
)


class Compiler(Visitor):
    def __init__(self) -> None:
        self._buffer: list[int] = []
        self._constants: list[list[int]] = [[1, ord('0')]]
        self.push = self._buffer.append

    def pushc(self, constant: list[int]) -> int:
        location = len(self._constants)
        self._constants.append(constant)
        return location

    reset = __init__

    def accept_number(self, expr: Number):
        size = len(expr.token.lexeme)
        constant = [size, *map(ord, expr.token.lexeme)]
        self.push(Instruction.LOAD_CONST)
        location = self.pushc(constant)
        self.push(location)

    def accept_plus(self, expr: Plus):
        expr.left.accept(self)
        expr.right.accept(self)
        self.push(Instruction.ADD)

    def accept_minus(self, expr: Minus):
        expr.left.accept(self)
        expr.right.accept(self)
        self.push(Instruction.SUBTRACT)

    def accept_slash(self, expr: Slash):
        expr.left.accept(self)
        expr.right.accept(self)
        self.push(Instruction.DIVIDE)

    def accept_power(self, expr: Power):
        expr.left.accept(self)
        expr.right.accept(self)
        self.push(Instruction.POWER)

    def accept_star(self, expr: Star):
        expr.left.accept(self)
        expr.right.accept(self)
        self.push(Instruction.MULTIPLY)

    def accept_group(self, expr: Group):
        expr.right.accept(self)

    def accept_uminus(self, expr: UMinus):
        self.push(Instruction.LOAD_CONST)
        self.push(0)
        expr.right.accept(self)
        self.push(Instruction.SUBTRACT)

    def accept_uplus(self, expr: UPlus):
        self.push(Instruction.LOAD_CONST)
        self.push(0)
        expr.right.accept(self)
        self.push(Instruction.ADD)

    def serialize_consts(self):
        constants = []
        for constant in self._constants:
            constants.extend(constant)
        constants.append(Instruction.EOS)
        return bytes(constants)

    def compile(self, root: Expression):
        self.reset()
        root.accept(self)
        self.push(Instruction.EOS)
        program = bytes(self._buffer)
        cosnts = self.serialize_consts()
        return bytes([*cosnts, *program])
