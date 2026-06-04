# 문제1. 식물 분류 프로젝트

## 문제 요약
- 아이리스 데이터셋으로 분류 모델을 만들고 성능을 평가하는 프로젝트형 문제입니다.
- 노트북 기반으로 데이터 탐색→시각화→학습→평가 순서로 진행됩니다.

## 핵심 파일
- `bbb.ipynb`: KNN 학습, 예측, Accuracy/Precision/Recall/F1, Confusion Matrix 출력

## 풀이에 필요한 정보
1. `pandas` DataFrame으로 feature/target 구조를 먼저 확인합니다.
2. `train_test_split(test_size=0.2, random_state=42)`로 실험을 재현합니다.
3. KNN 예측 결과를 정량 지표와 혼동행렬로 함께 해석하는 것이 핵심입니다.
4. 노트북 셀을 위에서 아래로 실행하면 됩니다.
