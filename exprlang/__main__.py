from .printer import ByteCodePrinter, ASTPrinter
from .exc import LexerError, ParserError
from .formatter import Formatter
from .evaluator import Evaluator
from .vm import VirtualMachine
from .compiler import Compiler
from .parser import Parser
from .lexer import Lexer

bytecodeprinter = ByteCodePrinter()
astprinter = ASTPrinter()
evaluator = Evaluator()
formatter = Formatter()
vm = VirtualMachine()
compiler = Compiler()
parser = Parser()
lexer = Lexer()


def _run(expr: str):
    try:
        tokens = lexer.scan(expr)
        print("TOKENS:")
        for token in tokens:
            print(f"  {token!s}")
        print()
        ast = parser.parse(tokens)
        print("AST:")
        astprinter.print(ast)
        print()
        bytecode = compiler.compile(ast)
        print(f"BYTECODE: {bytecode!r}")
        print("INSTRUCTIONS:")
        bytecodeprinter.print(bytecode, indent='  ')
        print()
        e_result = evaluator.eval(ast)
        v_result = vm.execute(bytecode)
        print(f"Expression: {formatter.format(ast)!r}")
        print(f"EvaluatorResult: {e_result!r}")
        print(f"VirtualMachineResult: {v_result!r}")
    except ParserError as e:
        print(f"ParsingError: {str(e)}")
    except LexerError as e:
        print(f"LexerError: {str(e)}")
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError: {str(e)}")


def main():
    print("Enter exit, quit, bye, q or press ctrl-c to exit.")
    while True:
        expr = input("> ")
        if expr in ("exit", "q", "quit", "bye"):
            break
        _run(expr)
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ...
    finally:
        print("Bye")
