#include <memory>
#include "nodes.hpp"

namespace snn {
#define _AcceptV(Klass)                   \
  void Klass::accept(Visitor &visitor) {  \
    visitor.accept(*this);                \
  }

#define _BinExpr(Klass) \
  Klass::Klass(std::unique_ptr<Expr> left, \
    std::unique_ptr<Expr> right)           \
    : left(std::move(left)),               \
      right(std::move(right)) { }          \
  _AcceptV(Klass)

#define _UnExpr(Klass)                       \
  Klass::Klass(std::unique_ptr<Expr> right)  \
    : right(std::move(right)) { }            \
  _AcceptV(Klass)

  _BinExpr(Add);
  _BinExpr(Mul);
  _BinExpr(Sub);
  _BinExpr(Div);
  _UnExpr(Pos);
  _UnExpr(Neg);

  Num::Num(double value):value(value) { }
  _AcceptV(Num);

#undef _BinExpr
#undef _UnExpr
#undef _AcceptV
}
