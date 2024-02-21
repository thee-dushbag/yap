from .typedef import ManagedStream as Stream
from .interpreter import Interpreter
from .printer import PrintExpression
from .pratts import expression
from .lexer import lex

p = PrintExpression()
i = Interpreter()

src = '60 / (1 ? 10 : 30)'
stream = Stream(lex(src))
expr = expression(stream)
result = i.eval(expr)
print(result)
print(p.tostr(expr))
