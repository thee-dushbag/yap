class Error(Exception):
    ...


class LexerError(Error):
    ...


class ParserError(Error):
    ...


class UnknownInstruction(Error):
    ...
