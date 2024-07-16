#pragma once

#include <memory>

namespace snn {
  struct Visitor;

  struct Expr {
    virtual void accept(Visitor&) = 0;
  };

  struct Add;
  struct Sub;
  struct Div;
  struct Mul;
  struct Neg;
  struct Pos;

  struct Num;

  struct Visitor {
    virtual void accept(Add&) = 0;
    virtual void accept(Div&) = 0;
    virtual void accept(Mul&) = 0;
    virtual void accept(Neg&) = 0;
    virtual void accept(Sub&) = 0;
    virtual void accept(Pos&) = 0;
    virtual void accept(Num&) = 0;
  };

#define _AcceptV \
  void accept(Visitor&)

#define _BinExpr(Klass)                \
  struct Klass: Expr {                 \
    std::unique_ptr<Expr> left, right; \
    Klass() = delete;                  \
    Klass(std::unique_ptr<Expr>,       \
      std::unique_ptr<Expr>);          \
    _AcceptV;                          \
  }

#define _UnExpr(Klass)                  \
  struct Klass: Expr {                  \
    std::unique_ptr<Expr> right;        \
    Klass() = delete;                   \
    Klass(std::unique_ptr<Expr>);       \
    _AcceptV;                           \
  }

  _BinExpr(Add);
  _BinExpr(Sub);
  _BinExpr(Div);
  _BinExpr(Mul);
  _UnExpr(Neg);
  _UnExpr(Pos);

  struct Num: Expr {
    double value;
    Num() = delete;
    Num(double);
    _AcceptV;
  };

#undef _BinExpr
#undef _UnExpr
#undef _AcceptV
}