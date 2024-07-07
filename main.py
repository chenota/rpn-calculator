#!/usr/bin/env python3

import curses
import argparse

# Single item in stack
class StackItem():
    def __init__(self, value, next):
        self.next = next
        self.value = value

# Stack manager
class Stack():
    def __init__(self):
        self.root = None
        self.size = 0
    def push(self, value):
        # New stack item pointing to current root
        new_item = StackItem(value, self.root)
        # Replace current root with new item
        self.root = new_item
        # Increment size
        self.size += 1
    def pop(self):
        # Don't pop empty stack
        if self.root is None:
            return None
        # Save return value
        retval = self.root.value 
        # Move root to next item down
        self.root = self.root.next 
        # Decrement size
        self.size -= 1
        # Return value
        return retval
    def to_string(self):
        as_list = [None] * self.size
        root = self.root
        for i in range(self.size):
            as_list[i] = str(root.value) 
            root = root.next
        return ' '.join(reversed(as_list))

# Parses cli arguments
class Parser(argparse.ArgumentParser):
    def __init__(self):
        # Initialize parent class
        super(Parser, self).__init__(
            prog='main.py',
            description='Calculator and visualizer for RPN arithmetic expressions'
        )
        # Add argument
        self.add_argument('expression', help='RPN expression to evaluate')

def main(stdscr, args):
    # Keypress w/o enter
    curses.cbreak(True)
    # Arrow keys
    stdscr.keypad(True)
    # Initialize stack
    stack = Stack()
    # Split input into list
    expression = args.expression.split()
    # Loop through expression
    for i, token in enumerate(expression):
        # Clear screen
        stdscr.clear()
        # Container for operation text
        operation_text = None
        # If token is an operation
        if token in ['+', '-', '*', '/']:
            # Check size
            if stack.size < 2:
                operation_text = 'Error: Need at least two numbers on the stack to perform arithmetic!'
            else:
                # Pop values
                val1 = stack.pop()
                val2 = stack.pop()
                # Perform operation
                final_val = None
                if token == '+': final_val = val2 + val1 
                elif token == '-': final_val = val2 - val1
                elif token == '*': final_val = val2 * val1 
                elif token == '/': final_val = val2 // val1
                # Push value back to stack
                stack.push(final_val)
                # Operation text
                operation_text = f'Popped {val2} and {val1} from stack, pushed {val2} {token} {val1} = {final_val} to stack'
        # Otherwise, check if number
        else:
            # Try to turn token into a number
            try:
                # Successfully turned token into integer, add token to stack
                stack.push(int(token))
                # Set operation text
                operation_text = f'Pushed {token} to stack'
            # Print error and break out of loop if not number
            except ValueError:
                operation_text = f'Error: {token} is not an integer or a valid operation!'
        # Redraw screen
        # Stack
        stdscr.addstr(0, 0, 'Stack')
        stdscr.addstr(1, 2, stack.to_string() + ' (top)')
        # Input
        stdscr.addstr(3, 0, 'Input')
        stdscr.addstr(4, 2, ' '.join(expression))
        stdscr.addstr(5, 2 + (2 * i), '^')
        # Operation
        stdscr.addstr(6, 0, 'Operation')
        stdscr.addstr(7, 2, operation_text)
        # Refresh
        stdscr.refresh
        # Wait for key
        stdscr.getkey()
        # Break if error
        if operation_text.startswith('Error'):
            break

if __name__ == '__main__':
    # Argument parser (need it out here to work correctly)
    args = Parser().parse_args()
    # Wrapped curses program
    curses.wrapper(main, args)