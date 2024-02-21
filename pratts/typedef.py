import typing as ty
from collections import deque

if ty.TYPE_CHECKING:
    from .token import Token
else:
    Token = type

# Objects used all over the project
# TokenStream = ty.Generator[Token, None, None]
TokenStream = ty.Iterator[Token]
_T_co = ty.TypeVar("_T_co", covariant=True)
_T_con = ty.TypeVar("_T_con", contravariant=True)


class Location(ty.NamedTuple):
    line: int
    column: int


class ManagedStream:
    def __init__(self, stream: TokenStream) -> None:
        self._queued: deque[Token] = deque()
        self._empty: bool = False
        self._stream = stream

    def _enq(self, enqueue: ty.Callable[[deque[Token], Token], None], unused: Token):
        enqueue(self._queued, unused)
        self._empty = False

    @property
    def empty(self) -> bool:
        return self._empty

    def __bool__(self) -> bool:
        return self._empty

    def put(self, unused: Token):
        self._enq(deque.append, unused)

    def putleft(self, unused: Token):
        self._enq(deque.appendleft, unused)

    def __iter__(self) -> ty.Self:
        return self

    def __next__(self) -> Token:
        if self._queued:
            return self._queued.popleft()
        try:
            return next(self._stream)
        except StopIteration:
            self._empty = True
            raise

    def peek(self) -> Token | None:
        tk = next(self, None)
        if tk is not None:
            self.putleft(tk)
        return tk


class Stringify(ty.Protocol[_T_con]):
    def tostr(self, thing: _T_con) -> str: ...
