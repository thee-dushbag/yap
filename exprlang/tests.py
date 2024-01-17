from .instructions import Instruction
from .token import Token, TokenType
from .evaluator import Evaluator
from .compiler import Compiler
from .parser import Parser
from .lexer import Lexer
from . import nodes
from .vm import VirtualMachine


def test_lexer():
    expr = "50 - +90 / 7 * 23 ^ (8 + -6)"
    lexer = Lexer()
    tokens = lexer.scan(expr)
    correct = [
        Token(TokenType.NUMBER, "50", 0),
        Token(TokenType.MINUS, "-", 3),
        Token(TokenType.PLUS, "+", 5),
        Token(TokenType.NUMBER, "90", 6),
        Token(TokenType.SLASH, "/", 9),
        Token(TokenType.NUMBER, "7", 11),
        Token(TokenType.STAR, "*", 13),
        Token(TokenType.NUMBER, "23", 15),
        Token(TokenType.POWER, "^", 18),
        Token(TokenType.LEFT, "(", 20),
        Token(TokenType.NUMBER, "8", 21),
        Token(TokenType.PLUS, "+", 23),
        Token(TokenType.MINUS, "-", 25),
        Token(TokenType.NUMBER, "6", 26),
        Token(TokenType.RIGHT, ")", 27),
        Token(TokenType.EOF, "", 28),
    ]
    assert correct == tokens


def test_parser():
    tokens = [
        Token(TokenType.NUMBER, "50", 0),
        Token(TokenType.MINUS, "-", 3),
        Token(TokenType.PLUS, "+", 5),
        Token(TokenType.NUMBER, "90", 6),
        Token(TokenType.SLASH, "/", 9),
        Token(TokenType.NUMBER, "7", 11),
        Token(TokenType.STAR, "*", 13),
        Token(TokenType.NUMBER, "23", 15),
        Token(TokenType.POWER, "^", 18),
        Token(TokenType.LEFT, "(", 20),
        Token(TokenType.NUMBER, "8", 21),
        Token(TokenType.PLUS, "+", 23),
        Token(TokenType.MINUS, "-", 25),
        Token(TokenType.NUMBER, "6", 26),
        Token(TokenType.RIGHT, ")", 27),
        Token(TokenType.EOF, "", 28),
    ]
    left = nodes.Number(tokens[10])
    right = nodes.Number(tokens[13])
    right = nodes.UMinus(tokens[12], right)
    root = nodes.Plus(left, tokens[11], right)
    root = nodes.Group(tokens[9], root)
    left = nodes.Number(tokens[7])
    root = nodes.Power(left, tokens[8], root)
    left = nodes.Number(tokens[3])
    left = nodes.UPlus(tokens[2], left)
    right = nodes.Number(tokens[5])
    left = nodes.Slash(left, tokens[4], right)
    root = nodes.Star(left, tokens[6], root)
    left = nodes.Number(tokens[0])
    root = nodes.Minus(left, tokens[1], root)

    parser = Parser()
    ast = parser.parse(tokens)
    assert root == ast


def test_evaluator():
    deps = Lexer(), Parser()

    def _genast(expr: str) -> nodes.Expression:
        return deps[1].parse(deps[0].scan(expr))

    exprs = (
        ("-3", -3),
        ("3 + 5", 8),
        ("4 * 7", 28),
        ("4 * 7 + 3", 31),
        ("2 ^ 2 ^ 2", 16),
        ("5 ^ 2 ^ 0.5", 5),
        ("9 / 10 / 10", 0.09),
        ("50 - +90 / 7 * 23 ^ (8 + -6)", -47260 / 7),
    )
    evaluator = Evaluator()
    for expr, ans in exprs:
        ast = _genast(expr)
        assert evaluator.eval(ast) == ans


def test_compiler():
    expr = "50 - +90 / 7 * 23 ^ (8 + -6)"
    deps = Lexer(), Parser()

    def _genast(expr: str) -> nodes.Expression:
        return deps[1].parse(deps[0].scan(expr))

    def _genconst(const: str):
        return [len(const), *map(ord, const)]

    consts = []
    for const in map(_genconst, ("0", "50", "90", "7", "23", "8", "6")):
        consts.extend(const)
    consts.append(Instruction.EOS)

    program = [
        Instruction.LOAD_CONST, 1,
        Instruction.LOAD_CONST, 0,
        Instruction.LOAD_CONST, 2,
        Instruction.ADD,
        Instruction.LOAD_CONST, 3,
        Instruction.DIVIDE,
        Instruction.LOAD_CONST, 4,
        Instruction.LOAD_CONST, 5,
        Instruction.LOAD_CONST, 0,
        Instruction.LOAD_CONST, 6,
        Instruction.SUBTRACT,
        Instruction.ADD,
        Instruction.POWER,
        Instruction.MULTIPLY,
        Instruction.SUBTRACT,
        Instruction.EOS,
    ]

    bytecode = bytes([*consts, *program])
    compiler = Compiler()
    ast = _genast(expr)
    gen_bytecode = compiler.compile(ast)
    assert gen_bytecode == bytecode


def test_virtual_machine():
    deps = Lexer(), Parser()

    def _genast(expr: str) -> nodes.Expression:
        return deps[1].parse(deps[0].scan(expr))

    exprs = (
        ("-3", -3),
        ("3 + 5", 8),
        ("4 * 7", 28),
        ("4 * 7 + 3", 31),
        ("1024 ^ 0.1", 2),
        ("2 ^ 2 ^ 2", 16),
        ("5 ^ 2 ^ 0.5", 5),
        ("9 / 10 / 10", 0.09),
        ("11111111 ^ 2", 123456787654321),
        ("50 - +90 / 7 * 23 ^ (8 + -6)", -47260 / 7),
    )

    vm = VirtualMachine()
    compiler = Compiler()
    for expr, ans in exprs:
        ast = _genast(expr)
        bytecode = compiler.compile(ast)
        assert vm.execute(bytecode) == ans
