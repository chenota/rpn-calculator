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
    def peek(self):
        if self.root is None:
            return None 
        return self.root.value
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
            prog='rpncalc.py',
            description='Calculator and visualizer for RPN arithmetic expressions'
        )
        # Add arguments
        self.add_argument('expression', help='RPN expression to evaluate')
        self.add_argument('--infix', help='Set this flag if the supplied expression is infix', action='store_true')

# Does a have higher or equal precedence than b?
def precedence(a, b):
    if a == '+' or a == '-':
        if b == '+' or b == '-':
            return True 
        elif b == '*' or b == '/':
            return False
    elif a == '*' or a == '/':
        if b == '*' or b == '/':
            return False
        elif b == '+' or b == '-':
            return True
    return None

# Convert infix expression to postfix expression
def infix_to_postfix(infix):
    postfix = []
    stack = Stack()
    for token in infix:
        if token in ['+', '-', '*', '/']:
            # Pop higher or equal precedence operators from stack, stop on ( or empty stack
            while precedence(stack.peek(), token):
                postfix.append(stack.pop())
            # Push operator to stack
            stack.push(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            # Add stack to postfix expression until encounter open paren
            while stack.peek() != '(':
                # If get all the way to end of stack w/o open paren, error
                if stack.peek() is None:
                    return None
                postfix.append(stack.pop())
            # Pop open paren
            stack.pop()
        else:
            postfix.append(token)
    # Pop rest of operators
    while stack.peek() is not None:
        postfix.append(stack.pop())
        # If encounter open paren, error
        if postfix[-1] == '(':
            return None
    return postfix

def main(stdscr, args):
    # Keypress w/o enter
    curses.cbreak(True)
    # Arrow keys
    stdscr.keypad(True)
    # Clear screen
    stdscr.clear()
    # Initialize stack
    stack = Stack()
    # Split input into list
    expression = args.expression.split()
    # Convert to postfix if is infix
    if args.infix:
        expression = infix_to_postfix(expression)
        if expression is None:
            stdscr.addstr(0, 0, 'Error: Invalid infix expresson. Press any key to continue...')
            stdscr.getkey()
            return
    # History
    history = [None] * len(expression)
    # Loop through expression
    i = 0
    while i < len(expression):
        # Clear screen
        stdscr.clear()
        # Container for operation text
        operation_text = None
        # Get token
        token = expression[i]
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
                # History
                history[i] = f'{token} {val2} {val1}'
                # Operation text
                operation_text = f'Popped {val2} and {val1} from stack, pushed {val2} {token} {val1} = {final_val} to stack'
        # Otherwise, check if number
        else:
            # Try to turn token into a number
            try:
                # Successfully turned token into integer, add token to stack
                stack.push(int(token))
                # History
                history[i] = token
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
        inpt_len = 0
        for j in range(i): inpt_len += len(expression[j])
        stdscr.addstr(5, 2 + i + inpt_len, '^' * len(expression[i]))
        # Operation
        stdscr.addstr(6, 0, 'Operation')
        stdscr.addstr(7, 2, operation_text)
        # Refresh
        stdscr.refresh()
        # Wait for key
        key = stdscr.getkey()
        # Break if error
        if operation_text.startswith('Error'):
            break
        # Handle key
        while True:
            if key == 'KEY_LEFT' and i > 0:
                # Undo operation
                stack.pop()
                # If was mathematical, push original values
                if history[i][0] in ['+', '-', '*', '/']:
                    stack.push(int(history[i].split()[1]))
                    stack.push(int(history[i].split()[2]))
                # Undo last operation
                stack.pop()
                # If was mathematical, push original values
                if history[i-1][0] in ['+', '-', '*', '/']:
                    stack.push(int(history[i-1].split()[1]))
                    stack.push(int(history[i-1].split()[2]))
                # Go back
                i -= 1
                break
            elif key == 'KEY_RIGHT':
                # Move forward
                i += 1
                break
            key = stdscr.getkey()
        # If last operation, print end screen
        if i >= len(expression):
            stdscr.clear()
            # Stack
            stdscr.addstr(0, 0, 'Stack')
            stdscr.addstr(1, 2, stack.to_string() + ' (top)')
            # Input
            stdscr.addstr(3, 0, 'Input')
            stdscr.addstr(4, 2, ' '.join(expression))
            # Done text
            stdscr.addstr(6, 0, 'Done! Press any key to exit...')
            stdscr.getkey()

if __name__ == '__main__':
    # Argument parser (need it out here to work correctly)
    args = Parser().parse_args()
    # Wrapped curses program
    curses.wrapper(main, args)