#pragma once

#include "nodes.hpp"
#include <sstream>

namespace snn {
#define _Acceptors   \
  void accept(Add&); \
  void accept(Num&); \
  void accept(Sub&); \
  void accept(Div&); \
  void accept(Mul&); \
  void accept(Neg&); \
  void accept(Pos&)  \

  class Evaluator: Visitor {
    double _result;
  public:
    _Acceptors;
    double eval(Expr&);
  };

  class Formatter: Visitor {
    std::stringstream _buffer;
  public:
    _Acceptors;
    std::string format(Expr&);
  };

#undef _Acceptors
}
