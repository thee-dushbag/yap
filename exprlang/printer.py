from .instructions import Instruction
from .exc import UnknownInstruction


class ByteCodePrinter:
    def __init__(self, bytecode: list[int] | bytes | None = None) -> None:
        self._constants: list[int | float] = []
        self._bytecode = bytecode or b""
        self._stop = len(self._bytecode)
        self._current = 0
        self._instructions = []
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
                case Instruction.ADD:
                    self.add()
                case Instruction.SUBTRACT:
                    self.subtract()
                case Instruction.MULTIPLY:
                    self.multiply()
                case Instruction.DIVIDE:
                    self.divide()
                case Instruction.POWER:
                    self.power()
                case Instruction.LOAD_CONST:
                    self.load_const()
                case unknown:
                    raise UnknownInstruction(unknown)
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
