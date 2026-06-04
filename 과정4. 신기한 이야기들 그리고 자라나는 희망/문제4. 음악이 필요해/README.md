# 문제4. 음악이 필요해

## 문제 요약
- 단일 연결 리스트와 원형 연결 리스트를 구현하고 재생목록 시나리오에 적용하는 자료구조 문제입니다.

## 핵심 파일
- `need_music.py`: `LinkedList`, `CircularList` 구현 및 데모
- `test_need_music.py`: 삽입/삭제/탐색/순환재생 동작 검증

## 풀이에 필요한 정보
1. `LinkedList.insert`는 `first`, `after`, 기본(last) 삽입을 지원합니다.
2. `CircularList.get_next`는 현재 포인터를 순환 이동하며 다음 곡을 반환합니다.
3. 타겟이 없는 `after` 삽입, 빈 리스트 처리 등 예외 케이스를 테스트로 확인할 수 있습니다.
4. 테스트 실행: `python test_need_music.py`
