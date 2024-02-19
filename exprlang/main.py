from .vm import VirtualMachine as _VirtualMachine
from .evaluator import Evaluator as _Evaluator
from .formatter import Formatter as _Formatter
from .compiler import Compiler as _Compiler
from .parser import Parser as _Parser
from .lexer import Lexer as _Lexer


class ExprEvaluator:
    # Facade to abstract away all the madness.
    def __init__(self) -> None:
        self._vm = _VirtualMachine()
        self._formatter = _Formatter()
        self._evaluator = _Evaluator()
        self._compiler = _Compiler()
        self._parser = _Parser()
        self._lexer = _Lexer()

    def _genast(self, expr: str):
        tokens = self._lexer.scan(expr)
        return self._parser.parse(tokens)

    def format(self, expr: str) -> str:
        ast = self._genast(expr)
        return self._formatter.format(ast)

    def eval(self, expr: str):
        ast = self._genast(expr)
        return self._evaluator.eval(ast)

    def exec(self, bytecode: bytes):
        return self._vm.execute(bytecode)

    def compile(self, expr: str):
        ast = self._genast(expr)
        return self._compiler.compile(ast)
