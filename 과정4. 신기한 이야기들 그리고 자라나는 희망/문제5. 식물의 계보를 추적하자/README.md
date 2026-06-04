# 문제5. 식물의 계보를 추적하자

## 문제 요약
- 이진 탐색 트리(BST)를 구현해 삽입/탐색/삭제(리프, 한 자식, 두 자식)를 처리하는 문제입니다.

## 핵심 파일
- `BinarySearchTree.py`: BST 구현
- `test_binary_search_tree.py`: 주요 연산 테스트

## 풀이에 필요한 정보
1. 중복 값은 삽입하지 않도록 `insert`에서 차단합니다.
2. 삭제 시 두 자식 노드는 오른쪽 서브트리 최소값으로 대체합니다.
3. `inorder()` 결과가 정렬 상태인지로 구현 정확도를 검증할 수 있습니다.
4. 테스트 실행: `python test_binary_search_tree.py`
