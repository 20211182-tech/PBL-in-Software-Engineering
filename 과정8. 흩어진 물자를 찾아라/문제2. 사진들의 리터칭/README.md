# 문제2. 사진들의 리터칭

## 문제 요약
- 노트북(`bbb.ipynb`)에서 아이리스(Iris) 데이터를 사용해 분류 모델(KNN)을 학습/평가하는 실습형 문제입니다.

## 핵심 파일
- `bbb.ipynb`: 데이터 확인, 시각화, 학습/예측, 성능평가(Accuracy/Precision/Recall/F1, Confusion Matrix)

## 풀이에 필요한 정보
1. `load_iris()`로 데이터 로드 후 `train_test_split`으로 학습/평가 데이터를 분리합니다.
2. `KNeighborsClassifier(n_neighbors=3)`로 모델을 학습합니다.
3. 혼동행렬 시각화로 클래스별 오분류를 확인합니다.
4. 노트북을 순서대로 실행하면 전체 분석 흐름을 재현할 수 있습니다.
