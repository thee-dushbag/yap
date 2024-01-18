from .vm import VirtualMachine as _VirtualMachine
from .evaluator import Evaluator as _Evaluator
from .formatter import Formatter as _Formatter
from .compiler import Compiler as _Compiler
from .parser import Parser as _Parser
from .lexer import Lexer as _Lexer


class ExprEvaluator:
    # Facade to abstract away all the complexity.
    def __init__(self) -> None:
        self._vm = _VirtualMachine()
        self._eval = _Evaluator()
        self._format = _Formatter()
        self._comp = _Compiler()
        self._pars = _Parser()
        self._lex = _Lexer()

    def _genast(self, expr: str):
        tokens = self._lex.scan(expr)
        return self._pars.parse(tokens)

    def format(self, expr: str) -> str:
        ast = self._genast(expr)
        return self._format.format(ast)

    def eval(self, expr: str):
        ast = self._genast(expr)
        return self._eval.eval(ast)

    def exec(self, bytecode: bytes):
        return self._vm.execute(bytecode)

    def compile(self, expr: str):
        ast = self._genast(expr)
        return self._comp.compile(ast)
