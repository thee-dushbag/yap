from .instructions import Instruction
from .exc import UnknownInstruction
from collections import defaultdict
from . import nodes


class ByteCodePrinter:
    def __init__(self, bytecode: list[int] | bytes | None = None) -> None:
        self._constants: list[int | float] = []
        self._bytecode = bytecode or b""
        self._stop = len(self._bytecode)
        self._current = 0
        self._instructions: list[str] = []
        self.push = self._instructions.append

    reset = __init__

    def peek(self) -> int:
        return self._bytecode[self._current]

    def advance(self) -> int:
        consumed = self.peek()
        self._current += 1
        return consumed

    def _load_constants(self):
        while self.peek() != Instruction.EOS:
            buffer = [chr(self.advance()) for _ in range(self.advance())]
            lexeme = "".join(buffer)
            type = float if "." in lexeme else int
            self._constants.append(type(lexeme))
        self.advance()
        self.push(f"CONSTANTS {self._constants}")

    def _execute(self):
        while self.peek() != Instruction.EOS:
            match self.peek():
                case Instruction.ADD:        self.add()
                case Instruction.POWER:      self.power()
                case Instruction.DIVIDE:     self.divide()
                case Instruction.MULTIPLY:   self.multiply()
                case Instruction.SUBTRACT:   self.subtract()
                case Instruction.LOAD_CONST: self.load_const()
                case unknown: raise UnknownInstruction(unknown)
        self.advance()

    def add(self):
        self.advance()
        self.push("ADD")

    def subtract(self):
        self.advance()
        self.push("SUBTRACT")

    def multiply(self):
        self.advance()
        self.push("MULTIPLY")

    def divide(self):
        self.advance()
        self.push("DIVIDE")

    def power(self):
        self.advance()
        self.push("POWER")

    def load_const(self):
        self.advance()
        location = self.advance()
        constant = self._constants[location]
        self.push(f"LOAD_CONST {location} [{constant}]")

    def join(self, indent: str) -> str:
        before = lambda i: indent + i
        indented = map(before, self._instructions)
        return "\n".join(indented)

    def print(
        self, bytecode: list[int] | bytes | None = None, /, *, indent: str | None = None
    ):
        self.reset(bytecode)
        self._load_constants()
        self._execute()
        indent = " " if indent is None else indent
        instructions = self.join(indent)
        print(instructions)


class ASTPrinter(nodes.Visitor[None]):
    def __init__(self) -> None:
        self._lines: dict[int, str] = defaultdict(lambda: "")
        self._column: int = 0
        self._line: int = 0

    @property
    def indent(self):
        return " " * self._column

    def advance(self, size: int = 1):
        self._column += size

    def accept_number(self, expr: nodes.Number):
        number = self.indent + expr.token.lexeme
        self.advance(len(expr.token.lexeme))
        self.addline(number)

    def addline(self, string: str):
        current = self._lines[self._line]
        current += string[len(current) :]
        self._lines[self._line] = current

    def _accept_binary(self, expr: nodes.Binary):
        head = self.indent + expr.operator.lexeme
        self.addline(head)
        self._line += 1
        expr.left.accept(self)
        self.advance()
        expr.right.accept(self)
        self._line -= 1

    def _accept_unary(self, expr: nodes.Unary):
        head = self.indent + expr.operator.lexeme
        self.addline(head)
        self._line += 1
        expr.right.accept(self)
        self._line -= 1

    def accept_plus(self, expr: nodes.Plus):
        return self._accept_binary(expr)

    def accept_minus(self, expr: nodes.Minus):
        return self._accept_binary(expr)

    def accept_power(self, expr: nodes.Power):
        return self._accept_binary(expr)

    def accept_slash(self, expr: nodes.Slash):
        return self._accept_binary(expr)

    def accept_star(self, expr: nodes.Star):
        return self._accept_binary(expr)

    def accept_group(self, expr: nodes.Group):
        return expr.right.accept(self)

    def accept_uminus(self, expr: nodes.UMinus):
        return self._accept_unary(expr)

    def accept_uplus(self, expr: nodes.UPlus):
        return self._accept_unary(expr)

    reset = __init__

    def join(self, root: nodes.Expression):
        self.reset()
        root.accept(self)
        lines = (self._lines[l] for l in sorted(self._lines))
        return "\n".join(lines)

    def print(self, root: nodes.Expression):
        print(self.join(root))
