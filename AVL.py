class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
class AVLTree:
    def __init__(self):
        self.root = None
    def get_height(self, node):
        if not node:
            return 0
        return node.height
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        return x
    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        return y
    def insert(self, key):
        print(f"\nInserting {key}...")
        print("Tree before insertion:")
        self.print_tree()
        self.root = self._insert(self.root, key)
        print("Tree after insertion and balancing:")
        self.print_tree()
    def _insert(self, node, key):
        if not node:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        return node
    def get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    def delete(self, key):
        print(f"\nDeleting {key}...")
        print("Tree before deletion:")
        self.print_tree()
        if self.search(key):
            self.root = self._delete(self.root, key)
        else:
            print(f"Key {key} not found in the tree.")
        print("Tree after deletion and balancing:")
        self.print_tree()
    def _delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self.get_min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        if node is None:
            return node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        return node
    def search(self, key):
        return self._search(self.root, key)
    def _search(self, node, key):
        if not node:
            return False
        if node.key == key:
            return True
        if key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)
    def print_tree(self):
        if not self.root:
            print("Empty tree")
            return
        self._print_tree(self.root, 0)
    def _print_tree(self, node, level):
        if node:
            self._print_tree(node.right, level + 1)
            print("    " * level + f"{node.key} (h={node.height}, b={self.get_balance(node)})")
            self._print_tree(node.left, level + 1)
    def balance_node(self, key):
        print(f"\nBalancing node with key {key}...")
        if not self.search(key):
            print(f"Key {key} not found in the tree.")
            return
        node = self._find_node(self.root, key)
        balance = self.get_balance(node)
        print(f"Node with key {key} has balance factor: {balance}")
        print("Tree before balancing:")
        self.print_tree()
        self.root = self._balance_node(self.root, key)
        print("Tree after balancing:")
        self.print_tree()
    def _find_node(self, node, key):
        if not node:
            return None
        if node.key == key:
            return node
        if key < node.key:
            return self._find_node(node.left, key)
        else:
            return self._find_node(node.right, key)
    def _balance_node(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self._balance_node(node.left, key)
        elif key > node.key:
            node.right = self._balance_node(node.right, key)
        else:
            balance = self.get_balance(node)
            if balance > 1:
                if self.get_balance(node.left) >= 0:
                    return self.right_rotate(node)
                else:
                    node.left = self.left_rotate(node.left)
                    return self.right_rotate(node)
            elif balance < -1:
                if self.get_balance(node.right) <= 0:
                    return self.left_rotate(node)
                else:
                    node.right = self.right_rotate(node.right)
                    return self.left_rotate(node)
        return node