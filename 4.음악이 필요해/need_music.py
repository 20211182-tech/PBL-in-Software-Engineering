class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data, position='last', target=None):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return True

        if position == 'first':
            new_node.next = self.head
            self.head = new_node
            return True

        if position == 'after':
            current = self.head
            while current is not None:
                if current.data == target:
                    new_node.next = current.next
                    current.next = new_node
                    return True
                current = current.next
            return False

        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node
        return True

    def delete(self, data):
        if self.head is None:
            return False

        if self.head.data == data:
            self.head = self.head.next
            return True

        previous = self.head
        current = self.head.next

        while current is not None:
            if current.data == data:
                previous.next = current.next
                return True
            previous = current
            current = current.next

        return False

    def get_list(self):
        items = []
        current = self.head

        while current is not None:
            items.append(current.data)
            current = current.next

        return items

    def search(self, data):
        current = self.head

        while current is not None:
            if current.data == data:
                return True
            current = current.next

        return False

    def display(self):
        items = self.get_list()
        if not items:
            print('The linked list is empty.')
            return
        print(' -> '.join(items))


class CircularList:
    def __init__(self):
        self.head = None
        self.current = None

    def insert(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.current = new_node
            new_node.next = new_node
            return True

        tail = self.head
        while tail.next != self.head:
            tail = tail.next

        tail.next = new_node
        new_node.next = self.head
        return True

    def delete(self, data):
        if self.head is None:
            return False

        if self.head.data == data:
            return self._delete_head()

        previous = self.head
        current = self.head.next

        while current != self.head:
            if current.data == data:
                previous.next = current.next
                if self.current == current:
                    self.current = current.next
                return True
            previous = current
            current = current.next

        return False

    def _delete_head(self):
        if self.head.next == self.head:
            self.head = None
            self.current = None
            return True

        tail = self.head
        while tail.next != self.head:
            tail = tail.next

        old_head = self.head
        self.head = self.head.next
        tail.next = self.head

        if self.current == old_head:
            self.current = self.head

        return True

    def get_next(self):
        if self.current is None:
            return None

        data = self.current.data
        self.current = self.current.next
        return data

    def search(self, data):
        if self.head is None:
            return False

        current = self.head
        while True:
            if current.data == data:
                return True

            current = current.next
            if current == self.head:
                return False

    def get_list(self):
        items = []

        if self.head is None:
            return items

        current = self.head
        while True:
            items.append(current.data)
            current = current.next
            if current == self.head:
                break

        return items

    def display(self):
        items = self.get_list()
        if not items:
            print('The circular list is empty.')
            return
        print(' -> '.join(items) + ' -> ...')


linkedlist = LinkedList
circularlist = CircularList


def print_result(message, result):
    print(f'{message}: {result}')


def run_linked_list_demo():
    print('[Simple Linked List]')
    playlist = linkedlist()

    playlist.insert('IU - Good Day')
    playlist.insert('BTS - Dynamite')
    playlist.insert('NewJeans - Hype Boy')
    playlist.insert('AKMU - Love Lee', position='first')
    playlist.insert(
        'SEVENTEEN - Super',
        position='after',
        target='BTS - Dynamite',
    )

    print_result('Playlist', playlist.get_list())
    print_result('Delete BTS - Dynamite', playlist.delete('BTS - Dynamite'))
    print_result('Search IU - Good Day', playlist.search('IU - Good Day'))
    print_result('Playlist after delete', playlist.get_list())
    print()


def run_circular_list_demo():
    print('[Circular Linked List]')
    player = circularlist()

    player.insert('IVE - I AM')
    player.insert('LE SSERAFIM - Perfect Night')
    player.insert('aespa - Drama')

    print_result('Playlist', player.get_list())
    print_result('Search aespa - Drama', player.search('aespa - Drama'))
    print_result(
        'Delete LE SSERAFIM - Perfect Night',
        player.delete('LE SSERAFIM - Perfect Night'),
    )
    print_result('Playlist after delete', player.get_list())

    print('Play next five songs')
    for _ in range(5):
        print(player.get_next())


def main():
    run_linked_list_demo()
    run_circular_list_demo()


if __name__ == '__main__':
    main()
