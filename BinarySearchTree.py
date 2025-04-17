import queue

class BinarySearchTree:

    class Node:

        def __init__(self):

            self.data = None
            self.left = None
            self.right = None

    def __init__(self):

        self.root = None

    def insert(self, data):

        if self.root is None:
            
            self.root = BinarySearchTree.Node(data)

        else:
            
            current = self.root
            inserted = False

            while not inserted:

                if data < current.data:

                    if current.left is not None:

                        current = current.left

                    else:

                        current.left = BinarySearchTree.Node(data)
                        inserted = True

                else:

                    if current.right is not None:

                        current = current.right

                    else:

                        current.right = BinarySearchTree.Node(data)
                        inserted = True

    def search(self, data):

        current = self.root

        while current is not None:

            if data < current.data:

                current = current.left

            elif data > current.data:

                current = current.right

            else:

                return current
            
        return None

    def printInOrder(self, subtree):

        if (subtree != None):

            self.printInOrder(subtree.left)
            print(subtree.data, end=" ")
            self.printInOrder(subtree.right)


    def print(self):

        self.printInOrder(self.root)
        print("")

    def printPreOrder(self):

        if (subtree != None):

            print(subtree.data, end=" ")
            self.printPreOrder(subtree.left)
            self.printPreOrder(subtree.right)

    def print(self):

        self.printPreOrder(self.root)
        print("")

    def printBreadthFirst(self):

        nodes = queue.Queue()

        if self.root is not None:

            nodes.put(self.root)

        while not nodes.empty():

            current = nodes.get()

            if current.left:

                nodes.put(current.left)

            if current.right:

                nodes.put(current.right)

            print(current.data, end=" ")
    