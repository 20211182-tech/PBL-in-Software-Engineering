# 문제2. 데이터 전처리 Min-Max

## 문제 요약
- 전복(Abalone) 데이터셋에 대해 Min-Max 정규화와 추가 전처리(Standardization, 샘플링)를 실습하는 문제입니다.

## 핵심 파일
- `ccc.ipynb`: Min-Max 스케일링, 표준화, 오버샘플링 실습
- `abalone.txt`: 원본 데이터
- `abalone_attributes.txt`: 컬럼 정의

## 풀이에 필요한 정보
1. `Sex`는 레이블로 분리하고 나머지 수치형 컬럼에 스케일러를 적용합니다.
2. `MinMaxScaler`로 [0, 1] 범위 정규화를 수행합니다.
3. 보너스로 `StandardScaler`, `RandomOverSampler`를 사용해 비교 실험을 진행합니다.
4. 노트북 경로에 맞게 데이터 파일 위치를 확인한 뒤 셀을 순차 실행하세요.
