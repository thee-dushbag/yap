# Yet Another Parser <sub><sub>👏</sub></sub>

### **YAP** project.

This project is an attempt to understand compilation, stack based virtual machines, bytecode generation, compactful executables (bytecode with advanced features) and executing bytecodes.  

This will also show the advantages of compilation over interpretation and hopefully will get my feet into compiler optimization. Specifically, simple compile time code evaluation (if all operands of an operation are available at compile time, then evaluate).

# Progress

- [x] Implement a basic Lexer.
- [x] Implement a basic Parser.
- [x] Implement a basic evaluator.
- [x] Design a simple VM with a few instructions.
- [x] Implement a simple AST Compiler.
- [x] Add a simple informative and usable REPR.
- [x] Add an instruction printer.
- [ ] Add an AST printer.
- [ ] Add a linter/expression formatter.
- [ ] Add more to this list.

# Hopes for the project.

I would like the project to
1. Evolve into a basic functional programming language.
2. Have good error handling and reporting.
3. Have nice little features like modules, generators, iterators, etc.

# Usage

With a simple REPR feature in the project, the exprlang can now be used by simply running.
```bash
$ python3 -m exprlang
```

This will lead to an expression prompt `> ` where you type in your expression, it will be lexed, parsed, compiled and evaluated using the VirtualMachine and the TreeWalkInterpreter (Evaluator) and the progress will be printed for examination.

![Example Usage](/assets/example.png)

# Disclaimer.
I'm not in any way whatsoever a master compiler/interpreter designer and this project will take a long time to finish. I do not recommend use of this in production calculator applications or whatever you want to use it in.  

This is a simple student project of how c/i works. See any errors or possible improvement (including implementations) please feel free to fork or open an issue.
