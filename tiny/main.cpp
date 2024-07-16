#include <iostream>
#include "nodes.hpp"
#include "visitors.hpp"
#include <memory>

auto main(int argc, char** argv) -> int {
  auto
    _6 = std::make_unique<snn::Num>(6),
    _7 = std::make_unique<snn::Num>(7),
    _8 = std::make_unique<snn::Num>(8),
    _9 = std::make_unique<snn::Num>(9),
    _10 = std::make_unique<snn::Num>(10),
    _100 = std::make_unique<snn::Num>(100);

  auto _8d9 = std::make_unique<snn::Div>(std::move(_8), std::move(_9));
  auto _7m8d9 = std::make_unique<snn::Mul>(std::move(_7), std::move(_8d9));
  auto _7m8d9m10 = std::make_unique<snn::Mul>(std::move(_7m8d9), std::move(_10));
  auto _6p7m8d9m10 = std::make_unique<snn::Add>(std::move(_6), std::move(_7m8d9m10));
  auto _6p7m8d9m10p100 = std::make_unique<snn::Add>(std::move(_6p7m8d9m10), std::move(_100));

  snn::Evaluator evaluator{ };
  snn::Formatter formatter{ };

  double result = evaluator.eval(*_6p7m8d9m10p100);
  std::string expression = formatter.format(*_6p7m8d9m10p100);
  std::cout << expression << " = " << result << '\n';

  _6 = std::make_unique<snn::Num>(6);
  _7 = std::make_unique<snn::Num>(7);
  _10 = std::make_unique<snn::Num>(10);
  auto _N6 = std::make_unique<snn::Neg>(std::move(_6));
  auto _N7 = std::make_unique<snn::Neg>(std::move(_7));
  auto _N7mN6 = std::make_unique<snn::Mul>(std::move(_N7), std::move(_N6));
  auto _P10 = std::make_unique<snn::Pos>(std::move(_10));
  auto _N7mN6pP10 = std::make_unique<snn::Add>(std::move(_N7mN6), std::move(_P10));

  result = evaluator.eval(*_N7mN6pP10);
  expression = formatter.format(*_N7mN6pP10);
  std::cout << expression << " = " << result << '\n';
}
