from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def main():
    iris = load_iris()

    print('1. iris 데이터셋 설명')
    print(iris.DESCR)

    print('2. target_names 출력')
    print(iris.target_names)
    print()

    print('3. feature_names 출력')
    print(iris.feature_names)
    print()

    print('4. data 정보 확인')
    print('data shape:', iris.data.shape)
    print('data ndim:', iris.data.ndim)
    print('data dtype:', iris.data.dtype)
    print('data sample:')
    print(iris.data[:5])
    print()

    print('5. target 정보 확인')
    print('target shape:', iris.target.shape)
    print('target ndim:', iris.target.ndim)
    print('target dtype:', iris.target.dtype)
    print('target sample:')
    print(iris.target[:5])
    print()

    print('6. train_test_split 사용')
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data,
        iris.target,
        test_size=0.25,
        random_state=0,
    )

    print('X_train shape:', X_train.shape)
    print('X_test shape:', X_test.shape)
    print('y_train shape:', y_train.shape)
    print('y_test shape:', y_test.shape)
    print()

    print('7. KNeighborsClassifier 학습')
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)

    print('8. 새로운 데이터 예측')
    new_data = [[5, 2.9, 1, 0.2]]
    prediction = knn.predict(new_data)
    print('예측할 데이터:', new_data)
    print('예측 결과 번호:', prediction)
    print('예측 결과 이름:', iris.target_names[prediction])
    print()

    print('9. 학습된 모델 평가')
    train_score = knn.score(X_train, y_train)
    test_score = knn.score(X_test, y_test)
    print('train score:', train_score)
    print('test score:', test_score)
    print()

    print('10. 데이터 분포 그래프')
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib이 설치되어 있지 않아 그래프는 출력하지 않습니다.')
        return

    for i in range(3):
        plt.scatter(
            iris.data[iris.target == i, 0],
            iris.data[iris.target == i, 1],
            label=iris.target_names[i],
        )

    plt.xlabel('sepal length (cm)')
    plt.ylabel('sepal width (cm)')
    plt.title('Iris Data Distribution')
    plt.legend(title='target')
    plt.show()


if __name__ == '__main__':
    main()
