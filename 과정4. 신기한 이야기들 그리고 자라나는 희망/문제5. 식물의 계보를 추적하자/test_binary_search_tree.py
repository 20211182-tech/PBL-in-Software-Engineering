import unittest

from BinarySearchTree import BinarySearchTree, binarytree


class TestBinarySearchTree(unittest.TestCase):
    def test_insert_and_find_values(self):
        tree = binarytree()
        for value in [50, 30, 70, 20, 40, 60, 80]:
            tree.insert(value)

        self.assertTrue(tree.find(20))
        self.assertTrue(tree.find(70))
        self.assertFalse(tree.find(90))
        self.assertEqual(tree.inorder(), [20, 30, 40, 50, 60, 70, 80])

    def test_delete_leaf_node(self):
        tree = BinarySearchTree()
        for value in [50, 30, 70, 20, 40]:
            tree.insert(value)

        self.assertTrue(tree.delete(20))
        self.assertFalse(tree.find(20))
        self.assertEqual(tree.inorder(), [30, 40, 50, 70])

    def test_delete_node_with_one_child(self):
        tree = BinarySearchTree()
        for value in [50, 30, 70, 60]:
            tree.insert(value)

        self.assertTrue(tree.delete(70))
        self.assertFalse(tree.find(70))
        self.assertEqual(tree.inorder(), [30, 50, 60])

    def test_delete_node_with_two_children(self):
        tree = BinarySearchTree()
        for value in [50, 30, 70, 20, 40, 60, 80]:
            tree.insert(value)

        self.assertTrue(tree.delete(50))
        self.assertFalse(tree.find(50))
        self.assertEqual(tree.inorder(), [20, 30, 40, 60, 70, 80])

    def test_duplicate_insert_is_ignored(self):
        tree = BinarySearchTree()
        tree.insert(30)
        tree.insert(30)

        self.assertEqual(tree.inorder(), [30])

    def test_delete_missing_value_returns_false(self):
        tree = BinarySearchTree()
        tree.insert(10)

        self.assertFalse(tree.delete(99))
        self.assertEqual(tree.inorder(), [10])


if __name__ == '__main__':
    unittest.main()
