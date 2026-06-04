# 문제1. 스페이스 타이타닉 사건

## 문제 요약
- `train.csv`/`test.csv` 승객 데이터를 이용해 `Transported`와의 관계를 분석하는 문제입니다.
- 코드(`spaceship_assignment.py`)는 상관계수 기반 핵심 변수 탐색과 연령/목적지 시각화를 수행합니다.

## 핵심 파일
- `spaceship_assignment.py`: 데이터 로드, 전처리, 상관계수 계산, 그래프 저장
- `train.csv`, `test.csv`: 원본 데이터
- `plot_age_transported.png`, `plot_destination_age_distribution.png`: 결과 그래프

## 풀이에 필요한 정보
1. `Transported`, `CryoSleep`, `VIP`를 불리언→숫자(1/0)로 변환 후 분석합니다.
2. `Age`는 10대~70대로 구간화하여 `Transported` 분포를 비교합니다.
3. `Destination`별 연령 분포는 누적 막대그래프로 확인합니다.
4. 실행: 해당 폴더에서 `python spaceship_assignment.py`
