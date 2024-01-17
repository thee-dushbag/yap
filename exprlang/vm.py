from .instructions import Instruction
from .exc import UnknownInstruction


class VirtualMachine:
    def __init__(self, bytecode: list[int] | bytes | None = None) -> None:
        self._stack = []
        self._constants: list[int | float] = []
        self._bytecode = bytecode or b""
        self._stop = len(self._bytecode)
        self.push = self._stack.append
        self.pop = self._stack.pop
        self._current = 0

    reset = __init__

    def execute(self, bytecode: list[int] | bytes | None = None):
        self.reset(bytecode)
        self._load_constants()
        self._execute()
        return self.pop()

    def _load_constants(self):
        while self.peek() != Instruction.EOS:
            buffer = [chr(self.advance()) for _ in range(self.advance())]
            lexeme = "".join(buffer)
            type = float if "." in lexeme else int
            self._constants.append(type(lexeme))
        self.advance()

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

    def peek(self) -> int:
        return self._bytecode[self._current]

    def advance(self) -> int:
        consumed = self.peek()
        self._current += 1
        return consumed

    def add(self):
        self.advance()
        right = self.pop()
        left = self.pop()
        self.push(left + right)

    def subtract(self):
        self.advance()
        right = self.pop()
        left = self.pop()
        self.push(left - right)

    def multiply(self):
        self.advance()
        right = self.pop()
        left = self.pop()
        self.push(left * right)

    def divide(self):
        right = self.pop()
        left = self.pop()
        if right == 0:
            raise ZeroDivisionError(f"'{left} / 0' at instruction {self._current}")
        self.advance()
        self.push(left / right)

    def power(self):
        self.advance()
        right = self.pop()
        left = self.pop()
        self.push(left**right)

    def load_const(self):
        self.advance()
        location = self.advance()
        constant = self._constants[location]
        self.push(constant)
