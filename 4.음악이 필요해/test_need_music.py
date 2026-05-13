import unittest

from need_music import circularlist, linkedlist


class TestLinkedList(unittest.TestCase):
    def test_insert_first_last_and_after_target(self):
        songs = linkedlist()
        songs.insert('Song B')
        songs.insert('Song A', position='first')
        songs.insert('Song D')
        songs.insert('Song C', position='after', target='Song B')

        self.assertEqual(
            songs.get_list(),
            ['Song A', 'Song B', 'Song C', 'Song D'],
        )

    def test_insert_after_missing_target_returns_false(self):
        songs = linkedlist()
        songs.insert('Song A')

        self.assertFalse(
            songs.insert('Song B', position='after', target='Missing Song')
        )
        self.assertEqual(songs.get_list(), ['Song A'])

    def test_delete_existing_and_missing_items(self):
        songs = linkedlist()
        songs.insert('Song A')
        songs.insert('Song B')
        songs.insert('Song C')

        self.assertTrue(songs.delete('Song A'))
        self.assertTrue(songs.delete('Song C'))
        self.assertFalse(songs.delete('Missing Song'))
        self.assertEqual(songs.get_list(), ['Song B'])


class TestCircularList(unittest.TestCase):
    def test_get_next_loops_through_items(self):
        songs = circularlist()
        songs.insert('Song A')
        songs.insert('Song B')
        songs.insert('Song C')

        self.assertEqual(
            [songs.get_next() for _ in range(5)],
            ['Song A', 'Song B', 'Song C', 'Song A', 'Song B'],
        )

    def test_search_and_delete_items(self):
        songs = circularlist()
        songs.insert('Song A')
        songs.insert('Song B')
        songs.insert('Song C')

        self.assertTrue(songs.search('Song B'))
        self.assertTrue(songs.delete('Song B'))
        self.assertFalse(songs.search('Song B'))
        self.assertEqual(songs.get_list(), ['Song A', 'Song C'])
        self.assertFalse(songs.delete('Missing Song'))

    def test_empty_circular_list_returns_none(self):
        songs = circularlist()

        self.assertIsNone(songs.get_next())
        self.assertFalse(songs.search('Song A'))
        self.assertFalse(songs.delete('Song A'))


if __name__ == '__main__':
    unittest.main()
