print("\nCourse code: BTP500 Data Structures and Algorithms")
print("Student name: Samin Ashraf")
print("Student ID: 140362229\n")

# Part 1.1

print("Part 1.1")

class StackUsingArrays:

    def __init__(self, max_size):

        self.stack = []
        self.max_size = max_size
        self.top = -1

    def push(self, item):

        if self.isFull():

            print("Stack is full. Cannot push more items.")

        else:

            self.top += 1
            self.stack.append(item)
            print(f"Pushed: {item}")

    def pop(self):

        if self.isEmpty():

            print("Stack is empty. Cannot pop.")
            return None

        else:

            item = self.stack.pop()
            self.top -= 1
            print(f"Popped: {item}")
            return item

    def top_element(self):

        if self.isEmpty():

            print("Stack is empty. No top element.")
            return None

        else:

            return self.stack[self.top]

    def isEmpty(self):

        return self.top == -1

    def isFull(self):

        return self.top == self.max_size - 1


# Demonstration
stack = StackUsingArrays(max_size=5)

fruits = ["Apples", "Bananas", "Grapes", "Berries", "Oranges"]
for fruit in fruits:

    stack.push(fruit)

print(f"Top element: {stack.top_element()}")

stack.pop()
stack.pop()

print(f"Is the stack empty? {stack.isEmpty()}")

print(f"Is the stack full? {stack.isFull()}")
print()

# Part 1.2

print("Part 1.2")

class Node:

    def __init__(self, data):

        self.data = data
        self.next = None


class Stack:

    def __init__(self):

        self.top = None
        self.size = 0

    def push(self, item):

        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
        print(f"Pushed: {item}")

    def pop(self):

        if self.isEmpty():

            print("Stack is empty. Cannot pop.")
            return None

        else:

            popped_item = self.top.data
            self.top = self.top.next
            self.size -= 1
            print(f"Popped: {popped_item}")
            return popped_item

    def top_element(self):

        if self.isEmpty():
            
            print("Stack is empty. No top element.")
            return None
        else:
            
            return self.top.data

    def isEmpty(self):

        return self.top is None

    def isFull(self):

        return False


# Demonstration
stack = Stack()

fruits = ["Apples", "Bananas", "Grapes", "Berries", "Oranges"]

for fruit in fruits:

    stack.push(fruit)

print(f"Top element: {stack.top_element()}")

stack.pop()
stack.pop()

print(f"Is the stack empty? {stack.isEmpty()}")
print(f"Is the stack full? {stack.isFull()}")