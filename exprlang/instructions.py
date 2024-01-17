import enum


class Instruction(enum.IntEnum):
    EOS = 0
    ADD = enum.auto()
    POWER = enum.auto()
    DIVIDE = enum.auto()
    MULTIPLY = enum.auto()
    SUBTRACT = enum.auto()
    LOAD_CONST = enum.auto()
