# Reverse Polish Notation Calculator

rpn-calc is a Reverse Polish Notation (RPN) calculator that demonstrates how RPN synergizes with stack machines by guiding you through a step-by-step calculation using a stack machine.

## How to Use

To use rpn-calc, simply run the included Python file (rpncalc.py) via the command line. You must specify the equation you want to calculate with a command line argument, like so:

```
python3 rpncalc.py '3 2 + 4 5 * -'
```

You may also enter an infix equation by setting the --infix flag, like so:

```
python3 rpncalc.py --infix '3 + 2 - ( 4 * 5 )'
```

If you specify an equation this way, your infix equation will be converted into a postfix (RPN) equvalent according to PEMDAS rules. Please note that _everything_ must be separated by whitespace, including parenthesis!

Upon running the program, you will be presented with a screen that looks like this:

```
Stack
  3 (top)

Input
  3 2 + 4 5 * -
  ^
Operation
  Pushed 3 to stack
```

You can use the right arrow key to advance through the input step-by-step, and you can use the left arrow key to navigate through the input backwards. This calculator works on integers and implements the four main mathematical operators (+, -, *, /); each operator must have exactly two operands.

## Compatability

rpn-calc relies on the curses library for its UI, which means rpn-calc should would out of the box on Mac and Linux machines, however Windows users will need to install curses in order for the program to work.

## Reverse Polish Notation

RPN is a postfix mathematical notation, where operators come after operands. For example, the mathematical expression "1 + 2" looks like "1 2 +" in RPN. RPN may be confusing to look at, however it has a couple of intersting properties:

1. The order of operations is entirely defined by the equation-writer, therefore there is no need for precedence rules like PEMDAS. RPN shares this property with s-expressions, its opposite counterpart.
2. Grouping is defined by the location of operators within the equation, therefore there is no need for grouping operators like parenthesis.

These properties can be demonstrated with an example equation:

|   |   |
|---|---|
|Infix                   | 2 * 5 + 3 * -1       |
|Infix w/ Grouping       | (2 * 5) + (3 * -1)   |
|S-Expression            | (+ (* 2 5) (* 3 -1)) |
|RPN                     | 2 5 * 3 -1 * +       |

Say you want to add five and three before performing any multiplication. Using normal (infix) notation, you would need to add parenthesis to manipulate precedence and using s-expressions, you would need an entirely new equation. However, using RPN, you simply need to re-arrange the operators. Here's that concept in action:

|   |   |
|---|---|
|Infix        | 2 * (5 + 3) * -1 |
|S-Expression | (* 2 (+ 5 3) -1) |
|RPN          | 2 5 3 + -1 * *   |

## Stack Machines

A stack machine is a type of computer or virtual machine that exclusively uses stacks for memory. The simplest kind of stack machine is a pushdown automata (PDA), which is a type of finite state machine that uses a stack to help dictate what edges to transition on. For an example of an important and nontrivial stack machine, see the [Python Bytecode Interpreter](https://devguide.python.org/internals/interpreter/). 

RPN equations are most naturally evaluated with a stack machine. The stack machine implemented in this program uses a single stack; when it encounters an operand, it pushes it onto the stack, and when it encounters an operator, it consumes the top two operands on the stack, and pushes the operation result back onto the stack.