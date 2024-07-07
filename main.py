#!/usr/bin/env python3

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