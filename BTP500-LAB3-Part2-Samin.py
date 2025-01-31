import time

print("\nCourse code: BTP500 Data Structures and Algorithms")
print("Student name: Samin Ashraf")
print("Student ID: 140362229\n")

# Singly-linked List class
class LinkedList:

    # Node class to store data
    class Node:

        # Initialization function for a node
        def __init__(self, data, next=None):

            self.data = data
            self.next = next

    # Initialization function for a singly-linked list
    def __init__(self):

        self.head = None

    # Function to insert data at the beginning of a singly-linked list
    def push_front(self, data):

        nn = self.Node(data, self.head)
        self.head = nn

    # Function to remove data at the end of a singly-linked list
    def pop_front(self):

        if self.head is not None:
            rm = self.head
            self.head = self.head.next
            del rm

    # Function to insert data at the end of a singly-linked list
    def push_back(self, data):

        nn = self.Node(data)

        if self.head is None:

            self.head = nn

        else:

            current = self.head

            while current.next is not None:

                current = current.next

            current.next = nn

    # Function to remove data at the end of a singly-linked list
    def pop_back(self):

        if self.head is not None:

            if self.head.next is None:

                del self.head
                self.head = None

            else:

                current = self.head

                while current.next.next is not None:

                    current = current.next

                del current.next
                current.next = None

    # Function to print the list
    def print_list(self):

        current = self.head

        while current is not None:

            print(current.data, end="")

            if current.next is not None:

                print(" -> ", end="")

            current = current.next

        print()

# Given:
# Strings: ["Grapes", "Banana", "Apples", "Pear", "Blackberry"]
# Integers: [910, 20, 340, 640, 550]
# Decimals: [11.5, 12.75, 3.25, 4.6, 15.0]

linked_list_strings = LinkedList()
linked_list_integers = LinkedList()
linked_list_decimals = LinkedList()

linked_list_strings.push_back("Grapes")
linked_list_strings.push_back("Banana")
linked_list_strings.push_back("Apples")
linked_list_strings.push_back("Pear")
linked_list_strings.push_back("Blackberry")

linked_list_strings.print_list()

linked_list_integers.push_back(910)
linked_list_integers.push_back(20)
linked_list_integers.push_back(340)
linked_list_integers.push_back(640)
linked_list_integers.push_back(550)

linked_list_integers.print_list()

linked_list_decimals.push_back(11.5)
linked_list_decimals.push_back(12.75)
linked_list_decimals.push_back(3.25)
linked_list_decimals.push_back(4.6)
linked_list_decimals.push_back(15.0)

linked_list_decimals.print_list()
print()

# Demonstrating bullet point 1
linked_list_strings.push_back("Grapes")
linked_list_strings.push_back("Banana")
linked_list_integers.push_back(910)
linked_list_integers.push_back(20)
linked_list_decimals.push_back(11.5)
linked_list_decimals.push_back(12.75)

print("Demonstrating bullet point 1")
linked_list_strings.print_list()
linked_list_integers.print_list()
linked_list_decimals.print_list()
print()

# Demonstrating bullet point 2
linked_list_strings.push_front("Apples")
linked_list_strings.push_front("Pear")
linked_list_strings.push_front("Blackberry")
linked_list_integers.push_front(550)
linked_list_integers.push_front(640)
linked_list_integers.push_front(340)
linked_list_decimals.push_front(15.0)
linked_list_decimals.push_front(4.6)
linked_list_decimals.push_front(3.25)

print("Demonstrating bullet point 2")
linked_list_strings.print_list()
linked_list_integers.print_list()
linked_list_decimals.print_list()
print()

# Demonstrating bullet point 3
linked_list_strings.pop_front()
linked_list_integers.pop_front()
linked_list_decimals.pop_front()

print("Demonstrating bullet point 3")
linked_list_strings.print_list()
linked_list_integers.print_list()
linked_list_decimals.print_list()
print()

# Demonstrating bullet point 4
linked_list_strings.pop_back()
linked_list_integers.pop_back()
linked_list_decimals.pop_back()

print("Demonstrating bullet point 4")
linked_list_strings.print_list()
linked_list_integers.print_list()
linked_list_decimals.print_list()
print()