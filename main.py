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
    def push(self, value):
        # New stack item pointing to current root
        new_item = StackItem(value, self.root)
        # Replace current root with new item
        self.root = new_item
    def pop(self):
        # Don't pop empty stack
        if self.root is None:
            return None
        # Save return value
        retval = self.root.value 
        # Move root to next item down
        self.root = self.root.next 
        # Return value
        return retval

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
    # Clear screen
    stdscr.clear()
    # Pause until get key
    stdscr.getkey()

if __name__ == '__main__':
    # Argument parser (need it out here to work correctly)
    parser = Parser()
    args = parser.parse_args()
    # Wrapped curses program
    curses.wrapper(main, args)