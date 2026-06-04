import unittest

from automatic_fertilizer_applicator import Stack, stack


class TestStack(unittest.TestCase):
    def test_push_pop_peek_and_empty(self):
        fertilizer_stack = stack()

        self.assertTrue(fertilizer_stack.empty())
        self.assertTrue(fertilizer_stack.push('Fertilizer-001'))
        self.assertTrue(fertilizer_stack.push('Fertilizer-002'))
        self.assertFalse(fertilizer_stack.empty())
        self.assertEqual(fertilizer_stack.peek(), 'Fertilizer-002')
        self.assertEqual(fertilizer_stack.pop(), 'Fertilizer-002')
        self.assertEqual(fertilizer_stack.pop(), 'Fertilizer-001')
        self.assertTrue(fertilizer_stack.empty())

    def test_pop_and_peek_empty_stack(self):
        fertilizer_stack = Stack()

        self.assertIsNone(fertilizer_stack.pop())
        self.assertIsNone(fertilizer_stack.peek())
        self.assertTrue(fertilizer_stack.empty())

    def test_push_limit_is_ten_items(self):
        fertilizer_stack = Stack()

        for number in range(1, 11):
            self.assertTrue(fertilizer_stack.push(f'Fertilizer-{number:03d}'))

        self.assertFalse(fertilizer_stack.push('Fertilizer-011'))
        self.assertEqual(fertilizer_stack.size(), 10)
        self.assertEqual(fertilizer_stack.peek(), 'Fertilizer-010')

    def test_visualize_shows_top_and_bottom(self):
        fertilizer_stack = Stack()
        fertilizer_stack.push('Fertilizer-001')
        fertilizer_stack.push('Fertilizer-002')

        self.assertEqual(
            fertilizer_stack.visualize(),
            [
                '[top] Fertilizer-002',
                '      Fertilizer-001 [bottom]',
            ],
        )


if __name__ == '__main__':
    unittest.main()
