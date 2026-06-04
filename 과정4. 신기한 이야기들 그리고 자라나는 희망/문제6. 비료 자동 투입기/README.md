# 문제6. 비료 자동 투입기

## 문제 요약
- 비료 투입 순서를 관리하는 스택(Stack) 자료구조를 구현하는 문제입니다.

## 핵심 파일
- `automatic_fertilizer_applicator.py`: `Stack` 구현(push/pop/peek/empty/visualize)
- `test_automatic_fertilizer_applicator.py`: 용량 제한, 빈 스택, 시각화 검증

## 풀이에 필요한 정보
1. 최대 크기(`max_size`, 기본 10)를 넘으면 push가 실패합니다.
2. 빈 스택의 `pop`, `peek`는 `None`을 반환하고 경고를 출력합니다.
3. `visualize()`는 top/bottom 라벨이 포함된 텍스트 배열을 반환합니다.
4. 테스트 실행: `python test_automatic_fertilizer_applicator.py`
