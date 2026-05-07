class stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        if item is None:
            print("item is None")
            return
        if len(self.stack) >= 10:
            print("stack is full")
            return
        self.stack.append(item)
        
    def pop(self):
        if len(self.stack) == 0:
            print("stack is empty")
            return None
        return self.stack.pop()

    def peek(self):
        if len(self.stack) == 0:
            return None
        return self.stack[-1]
    
    def is_empty(self):
        return len(self.stack) == 0

def main():
    s = stack()
    s.push(1)
    s.push(2)
    s.push(3)
    print(s.peek())  # 3
    print(s.pop())   # 3
    print(s.peek())  # 2
    print(s.is_empty())  # False
    s.pop()
    s.pop()
    print(s.is_empty())  # True