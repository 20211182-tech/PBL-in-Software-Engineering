class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
            return True

        return self._insert_node(self.root, data)

    def _insert_node(self, node, data):
        if data == node.data:
            return False

        if data < node.data:
            if node.left is None:
                node.left = Node(data)
                return True
            return self._insert_node(node.left, data)

        if node.right is None:
            node.right = Node(data)
            return True
        return self._insert_node(node.right, data)

    def find(self, data):
        return self._find_node(self.root, data) is not None

    def _find_node(self, node, data):
        if node is None:
            return None

        if data == node.data:
            return node

        if data < node.data:
            return self._find_node(node.left, data)

        return self._find_node(node.right, data)

    def delete(self, data):
        self.root, deleted = self._delete_node(self.root, data)
        return deleted

    def _delete_node(self, node, data):
        if node is None:
            return None, False

        if data < node.data:
            node.left, deleted = self._delete_node(node.left, data)
            return node, deleted

        if data > node.data:
            node.right, deleted = self._delete_node(node.right, data)
            return node, deleted

        if node.left is None:
            return node.right, True

        if node.right is None:
            return node.left, True

        min_node = self._find_min(node.right)
        node.data = min_node.data
        node.right, _ = self._delete_node(node.right, min_node.data)
        return node, True

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder(self):
        result = []
        self._collect_inorder(self.root, result)
        return result

    def _collect_inorder(self, node, result):
        if node is None:
            return

        self._collect_inorder(node.left, result)
        result.append(node.data)
        self._collect_inorder(node.right, result)


binarytree = BinarySearchTree


def run_demo():
    plants = binarytree()
    plant_numbers = [50, 30, 70, 20, 40, 60, 80]

    for number in plant_numbers:
        plants.insert(number)

    print('Plant family tree:', plants.inorder())
    print('Find plant 40:', plants.find(40))
    print('Find plant 90:', plants.find(90))
    print('Delete plant 30:', plants.delete(30))
    print('Plant family tree after delete:', plants.inorder())


if __name__ == '__main__':
    run_demo()
