class Stack:
    def __init__(self, max_size=10):
        self.max_size = max_size
        self.items = []

    def push(self, item):
        if len(self.items) >= self.max_size:
            print('Warning: stack is full. The item was not added.')
            return False

        self.items.append(item)
        return True

    def pop(self):
        if self.empty():
            print('Warning: stack is empty. There is no item to pop.')
            return None

        return self.items.pop()

    def empty(self):
        return len(self.items) == 0

    def peek(self):
        if self.empty():
            print('Warning: stack is empty. There is no item to peek.')
            return None

        return self.items[-1]

    def size(self):
        return len(self.items)

    def visualize(self):
        if self.empty():
            return ['[empty stack]']

        lines = []
        reversed_items = list(reversed(self.items))

        for index, item in enumerate(reversed_items):
            label = '      '
            if index == 0:
                label = '[top] '

            line = f'{label}{item}'
            if index == len(reversed_items) - 1:
                line = f'{line} [bottom]'
            lines.append(line)

        return lines

    def print_stack(self):
        for line in self.visualize():
            print(line)


stack = Stack


def run_demo():
    fertilizer_stack = stack()

    print('[Push fertilizer items]')
    for number in range(1, 12):
        item = f'Fertilizer-{number:03d}'
        result = fertilizer_stack.push(item)
        print(f'push {item}: {result}')

    print()
    print('[Current stack]')
    fertilizer_stack.print_stack()

    print()
    print('[Peek and pop]')
    print('peek:', fertilizer_stack.peek())
    print('pop:', fertilizer_stack.pop())
    print('pop:', fertilizer_stack.pop())
    print('empty:', fertilizer_stack.empty())

    print()
    print('[Stack after pop]')
    fertilizer_stack.print_stack()


if __name__ == '__main__':
    run_demo()
