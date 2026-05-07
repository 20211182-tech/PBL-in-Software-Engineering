"""
음악 플레이리스트를 관리하는 연결 리스트 구현
- 단순 연결 리스트 (LinkedList)
- 원형 연결 리스트 (CircularList)
"""
from typing import Optional, Any


class Node:
    """노드 클래스: 데이터와 다음 노드 포인터를 저장"""

    def __init__(self, data: Any):
        self.data: Any = data
        self.next: Optional['Node'] = None


class LinkedList:
    """단순 연결 리스트 클래스"""

    def __init__(self) -> None:
        self.head: Optional[Node] = None

    def insert(self, data: Any, position: Optional[str] = None, target: Optional[Any] = None) -> None:
        """
        연결 리스트에 새로운 항목 추가
        Args:
            data: 추가할 데이터
            position: 'first' (처음), 'last' (마지막), 'after' (특정 노드 뒤)
            target: position이 'after'일 때 기준이 되는 노드의 데이터
        """
        new_node = Node(data)

        # 리스트가 비어있는 경우
        if self.head is None:
            self.head = new_node
            return

        # 첫번째 위치에 삽입
        if position == 'first':
            new_node.next = self.head
            self.head = new_node
            return

        # 마지막 위치에 삽입
        if position == 'last' or position is None:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            return

        # 특정 노드 뒤에 삽입
        if position == 'after' and target is not None:
            current = self.head
            while current and current.data != target:
                current = current.next

            if current is None:
                print(f"'{target}'을(를) 찾을 수 없습니다.")
                return

            new_node.next = current.next
            current.next = new_node
            return

    def delete(self, data: Any) -> None:
        """
        연결 리스트에서 지정한 데이터 삭제
        Args:
            data: 삭제할 데이터
        """
        if self.head is None:
            print('리스트가 비어 있습니다.')
            return

        # 헤드 노드 삭제
        if self.head.data == data:
            self.head = self.head.next
            print(f"'{data}'을(를) 삭제했습니다.")
            return

        # 다른 노드 삭제
        current = self.head
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                print(f"'{data}'을(를) 삭제했습니다.")
                return
            current = current.next

        print(f"'{data}'을(를) 찾을 수 없습니다.")

    def get_list(self) -> list[Any]:
        """처음부터 끝까지 순차적으로 전체 항목 반환"""
        result: list[Any] = []
        current: Optional[Node] = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def display(self) -> None:
        """리스트의 모든 항목 출력"""
        items: list[Any] = self.get_list()
        if not items:
            print('리스트가 비어 있습니다.')
        else:
            print(' -> '.join(str(item) for item in items))

    def search(self, data: Any) -> bool:
        """
        특정 데이터 검색
        Args:
            data: 검색할 데이터
        Returns:
            찾으면 True, 없으면 False
        """
        current: Optional[Node] = self.head
        while current is not None:
            if current.data == data:
                return True
            current = current.next
        return False


class CircularList:
    """원형 연결 리스트 클래스"""

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.current: Optional[Node] = None

    def insert(self, data: Any) -> None:
        """
        원형 연결 리스트에 새로운 항목 추가
        Args:
            data: 추가할 데이터
        """
        new_node = Node(data)

        # 첫 번째 노드 삽입
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            self.current = new_node
            return

        # 마지막 노드에 삽입
        current: Optional[Node] = self.head
        while current is not None and current.next != self.head:
            current = current.next

        if current is not None:
            current.next = new_node
        new_node.next = self.head

    def delete(self, data: Any) -> None:
        """
        원형 연결 리스트에서 특정 항목 삭제
        Args:
            data: 삭제할 데이터
        """
        if self.head is None:
            print('리스트가 비어 있습니다.')
            return

        # 헤드 노드 삭제
        if self.head.data == data:
            if self.head.next == self.head:
                self.head = None
                self.current = None
                print(f"'{data}'을(를) 삭제했습니다.")
                return
            else:
                current: Optional[Node] = self.head
                while current is not None and current.next != self.head:
                    current = current.next
                if current is not None and self.head is not None:
                    current.next = self.head.next
                    self.head = self.head.next
                    self.current = self.head
                print(f"'{data}'을(를) 삭제했습니다.")
                return

        # 다른 노드 삭제
        current: Optional[Node] = self.head
        prev: Optional[Node] = None
        while True:
            if current is not None and current.data == data:
                if prev is not None:
                    prev.next = current.next
                if self.current == current:
                    self.current = current.next if current.next != self.head else self.head
                print(f"'{data}'을(를) 삭제했습니다.")
                return

            prev = current
            current = current.next if current is not None else None

            if current == self.head or current is None:
                print(f"'{data}'을(를) 찾을 수 없습니다.")
                return

    def get_next(self) -> Optional[Any]:
        """다음 항목으로 이동하고 현재 항목 반환"""
        if self.head is None or self.current is None:
            return None

        data: Any = self.current.data
        self.current = self.current.next
        return data

    def search(self, data: Any) -> bool:
        """
        원형 연결 리스트에서 항목 검색
        Args:
            data: 검색할 데이터
        Returns:
            찾으면 True, 없으면 False
        """
        if self.head is None:
            return False

        current: Optional[Node] = self.head
        while True:
            if current is not None and current.data == data:
                return True
            current = current.next if current is not None else None
            if current == self.head:
                break

        return False

    def display(self) -> None:
        """원형 연결 리스트의 모든 항목 출력"""
        if self.head is None:
            print('리스트가 비어 있습니다.')
            return

        items: list[Any] = []
        current: Optional[Node] = self.head
        while True:
            if current is not None:
                items.append(current.data)
                current = current.next
            if current == self.head:
                break

        print(' -> '.join(str(item) for item in items) + ' -> (다시 처음으로)')


def main() -> None:
    """단순 연결 리스트 테스트"""
    print('=' * 50)
    print('단순 연결 리스트 테스트')
    print('=' * 50)

    playlist = LinkedList()

    print('\n1. 음악 추가 (마지막 위치)')
    playlist.insert('아이유 - 좋은날')
    playlist.insert('싸이 - 강남스타일')
    playlist.insert('비 - 누누누')
    playlist.display()

    print('\n2. 첫번째 위치에 추가')
    playlist.insert('BTS - Dynamite', position='first')
    playlist.display()

    print('\n3. 특정 위치(\'싸이 - 강남스타일\' 뒤)에 추가')
    playlist.insert('말리 - Happier Than Ever', position='after',
                    target='싸이 - 강남스타일')
    playlist.display()

    print('\n4. 전체 리스트 조회 (get_list)')
    items = playlist.get_list()
    print(f'리스트 항목: {items}')

    print('\n5. 특정 음악 검색')
    search_song = '비 - 누누누'
    found = playlist.search(search_song)
    print(f"'{search_song}' 검색 결과: {found}")

    print('\n6. 음악 삭제')
    playlist.delete('싸이 - 강남스타일')
    playlist.display()

    print('\n7. 없는 음악 삭제 시도')
    playlist.delete('존재하지 않는 노래')

    print('\n' + '=' * 50)
    print('원형 연결 리스트 테스트')
    print('=' * 50)

    circular_playlist = CircularList()

    print('\n1. 음악 추가')
    circular_playlist.insert('IU - LILAC')
    circular_playlist.insert('NewJeans - Attention, Please')
    circular_playlist.insert('SEVENTEEN - GOD\'S MENU')
    circular_playlist.insert('TWICE - Set me Free')
    circular_playlist.display()

    print('\n2. 원형 리스트에서 순차 이동 (get_next)')
    print('순차적으로 5번 이동:')
    for _ in range(5):
        song = circular_playlist.get_next()
        print(f'  현재 곡: {song}')

    print('\n3. 특정 음악 검색')
    search_song = 'SEVENTEEN - GOD\'S MENU'
    found = circular_playlist.search(search_song)
    print(f"'{search_song}' 검색 결과: {found}")

    search_song = '없는 노래 - TEST'
    found = circular_playlist.search(search_song)
    print(f"'{search_song}' 검색 결과: {found}")

    print('\n4. 음악 삭제')
    circular_playlist.delete('NewJeans - Attention, Please')
    circular_playlist.display()

    print('\n5. 다시 순차 이동 (get_next)')
    print('순차적으로 4번 이동:')
    for _ in range(4):
        song = circular_playlist.get_next()
        print(f'  현재 곡: {song}')

    print('\n6. 없는 음악 삭제 시도')
    circular_playlist.delete('존재하지 않는 곡')


if __name__ == '__main__':
    main()
    
