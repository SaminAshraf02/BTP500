class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
class BinarySearchTree:
    def __init__(self):
        self.root = None
    def insert(self, value):
        if not self.root:
            self.root = Node(value)
            return
        def _insert(node, value):
            if value < node.value:
                if node.left:
                    _insert(node.left, value)
                else:
                    node.left = Node(value)
            else:
                if node.right:
                    _insert(node.right, value)
                else:
                    node.right = Node(value)
        _insert(self.root, value)
    def search(self, value):
        def _search(node, value):
            if not node:
                return False
            if node.value == value:
                return True
            if value < node.value:
                return _search(node.left, value)
            return _search(node.right, value)
        return _search(self.root, value)
    def inorder(self):
        result = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node.value)
                _inorder(node.right)
        _inorder(self.root)
        return result
    def preorder(self):
        result = []
        def _preorder(node):
            if node:
                result.append(node.value)
                _preorder(node.left)
                _preorder(node.right)
        _preorder(self.root)
        return result
    def postorder(self):
        result = []
        def _postorder(node):
            if node:
                _postorder(node.left)
                _postorder(node.right)
                result.append(node.value)
        _postorder(self.root)
        return result
    def breadthfirst(self):
        if not self.root:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result
    def depthfirst(self):
        # Using pre-order traversal for depth-first search
        return self.preorder()
    def printInOrder(self):
        print("In-order traversal:", self.inorder())
    def printPreOrder(self):
        print("Pre-order traversal:", self.preorder())
    def printBreadthFirst(self):
        print("Breadth-first traversal:", self.breadthfirst())