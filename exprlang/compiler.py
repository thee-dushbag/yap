from .instructions import Instruction
from . import nodes


class Compiler(nodes.Visitor[None]):
    def __init__(self) -> None:
        self._constants: list[list[int]] = [[1, ord("0")]]
        self._buffer: list[int] = []
        self.push = self._buffer.append

    def pushc(self, constant: list[int]) -> int:
        location = len(self._constants)
        self._constants.append(constant)
        return location

    reset = __init__

    def accept_number(self, expr: nodes.Number):
        size = len(expr.token.lexeme)
        constant = [size, *map(ord, expr.token.lexeme)]
        self.push(Instruction.LOAD_CONST)
        location = self.pushc(constant)
        self.push(location)

    def accept_plus(self, expr: nodes.Plus):
        expr.left.accept(self)
        expr.right.accept(self)
        self.push(Instruction.ADD)

    def accept_minus(self, expr: nodes.Minus):
        expr.left.accept(self)
        expr.right.accept(self)
        self.push(Instruction.SUBTRACT)

    def accept_slash(self, expr: nodes.Slash):
        expr.left.accept(self)
        expr.right.accept(self)
        self.push(Instruction.DIVIDE)

    def accept_power(self, expr: nodes.Power):
        expr.left.accept(self)
        expr.right.accept(self)
        self.push(Instruction.POWER)

    def accept_star(self, expr: nodes.Star):
        expr.left.accept(self)
        expr.right.accept(self)
        self.push(Instruction.MULTIPLY)

    def accept_group(self, expr: nodes.Group):
        expr.right.accept(self)

    def accept_uminus(self, expr: nodes.UMinus):
        self.push(Instruction.LOAD_CONST)
        self.push(0)
        expr.right.accept(self)
        self.push(Instruction.SUBTRACT)

    def accept_uplus(self, expr: nodes.UPlus):
        self.push(Instruction.LOAD_CONST)
        self.push(0)
        expr.right.accept(self)
        self.push(Instruction.ADD)

    def serialize_consts(self):
        from itertools import chain

        constants = chain.from_iterable(self._constants)
        return bytes(chain(constants, (Instruction.EOS,)))

    def compile(self, root: nodes.Expression):
        self.reset()
        root.accept(self)
        self.push(Instruction.EOS)
        program = bytes(self._buffer)
        cosnts = self.serialize_consts()
        return cosnts + program
