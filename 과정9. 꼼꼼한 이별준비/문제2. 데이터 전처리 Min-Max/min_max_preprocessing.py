from collections import Counter
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'abalone.txt'
ATTR_FILE = BASE_DIR / 'abalone_attributes.txt'


def main():
    with open(ATTR_FILE, encoding='utf-8') as file:
        columns = file.read().splitlines()

    df = pd.read_csv(DATA_FILE, header=None, names=columns)

    print('1. abalone 데이터 확인')
    print(df.head())
    print()

    label = df['Sex']
    data = df.drop(columns=['Sex'])

    print('2. label 확인')
    print(label.head())
    print()

    print('3. Sex 컬럼을 삭제한 data 확인')
    print(data.head())
    print()

    print('4. 원본 데이터 최대값')
    print(data.max())
    print()

    print('5. 원본 데이터 최소값')
    print(data.min())
    print()

    print('6. 직접 수식으로 Min-Max Scaling')
    min_value = data.min()
    max_value = data.max()
    manual_min_max = (data - min_value) / (max_value - min_value)
    print(manual_min_max.head())
    print()

    print('7. sklearn MinMaxScaler 사용')
    min_max_scaler = MinMaxScaler()
    scaled_data = min_max_scaler.fit_transform(data)
    scaled_df = pd.DataFrame(scaled_data, columns=data.columns)
    print(scaled_df.head())
    print()

    print('8. StandardScaler 사용')
    standard_scaler = StandardScaler()
    standard_data = standard_scaler.fit_transform(data)
    standard_df = pd.DataFrame(standard_data, columns=data.columns)
    print(standard_df.head())
    print()

    print('9. label 개수 확인')
    print(Counter(label))
    print()

    sampling_df = data.copy()
    sampling_df['label'] = label

    print('10. Random Over Sampling 직접 구현')
    max_count = label.value_counts().max()
    over_list = []

    for name in label.unique():
        group = sampling_df[sampling_df['label'] == name]
        over_group = group.sample(
            max_count,
            replace=True,
            random_state=42,
        )
        over_list.append(over_group)

    over_sampling_df = pd.concat(over_list)
    over_label = over_sampling_df['label']
    over_data = over_sampling_df.drop(columns=['label'])

    print('over data shape:', over_data.shape)
    print('over label:', Counter(over_label))
    print()

    print('11. Random Under Sampling 직접 구현')
    min_count = label.value_counts().min()
    under_list = []

    for name in label.unique():
        group = sampling_df[sampling_df['label'] == name]
        under_group = group.sample(
            min_count,
            replace=False,
            random_state=42,
        )
        under_list.append(under_group)

    under_sampling_df = pd.concat(under_list)
    under_label = under_sampling_df['label']
    under_data = under_sampling_df.drop(columns=['label'])

    print('under data shape:', under_data.shape)
    print('under label:', Counter(under_label))
    print()

    print('12. SMOTE 사용')
    try:
        from imblearn.over_sampling import SMOTE
    except ImportError:
        print('imblearn이 설치되어 있지 않아 SMOTE는 실행하지 않습니다.')
        return

    smote = SMOTE(random_state=42)
    smote_data, smote_label = smote.fit_resample(data, label)

    print('smote data shape:', smote_data.shape)
    print('smote label:', Counter(smote_label))


if __name__ == '__main__':
    main()
