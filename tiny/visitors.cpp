#include "nodes.hpp"
#include "visitors.hpp"
#include <sstream>

namespace snn {
#define _AcceptBin(Klass, _op_) \
    void Evaluator::accept(Klass& expr) { \
      expr.left->accept(*this); \
      double left = this->_result; \
      expr.right->accept(*this); \
      this->_result = left _op_ this->_result; \
    }

#define _AcceptUn(Klass, _op_) \
    void Evaluator::accept(Klass& expr) { \
      expr.right->accept(*this); \
      this->_result = _op_ this->_result; \
    }

    _AcceptBin(Add, +);
    _AcceptBin(Mul, *);
    _AcceptBin(Div, / );
    _AcceptBin(Sub, -);
    _AcceptUn(Pos, +);
    _AcceptUn(Neg, -);

#undef _AcceptBin
#undef _AcceptUn

    void Evaluator::accept(Num& expr) {
      this->_result = expr.value;
    }

    double Evaluator::eval(Expr& expr) {
      expr.accept(*this);
      return this->_result;
    }

#define _AcceptBin(Klass, _op_) \
    void Formatter::accept(Klass& expr) { \
      expr.left->accept(*this); \
      this->_buffer << " " #_op_ " "; \
      expr.right->accept(*this); \
    }

#define _AcceptUn(Klass, _op_) \
    void Formatter::accept(Klass& expr) { \
      this->_buffer << #_op_; \
      expr.right->accept(*this); \
    }

    _AcceptBin(Add, +);
    _AcceptBin(Mul, *);
    _AcceptBin(Div, / );
    _AcceptBin(Sub, -);
    _AcceptUn(Pos, +);
    _AcceptUn(Neg, -);

#undef _AcceptBin
#undef _AcceptUn

    void Formatter::accept(Num& expr) {
      this->_buffer << expr.value;
    }

    std::string Formatter::format(Expr& expr) {
      this->_buffer = { };
      expr.accept(*this);
      return this->_buffer.str();
    }
}
