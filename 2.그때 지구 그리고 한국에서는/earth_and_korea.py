import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / 'korea_earth.csv'
PLOT_PATH = BASE_DIR / 'earth_korea_gender_age_trend.png'
YEAR_COLUMN = ('시점', '시점', '시점', '시점')


def load_dataframe() -> pd.DataFrame:
    """Load the CSV exported from KOSIS with a 4-level header."""
    return pd.read_csv(CSV_PATH, encoding='cp949', header=[0, 1, 2, 3])


def prepare_long_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Keep only '일반가구원' columns and convert them to long format."""
    value_cols = [
        col
        for col in raw_df.columns
        if isinstance(col, tuple) and col[3] == '일반가구원'
    ]

    long_df = raw_df.melt(
        id_vars=[YEAR_COLUMN],
        value_vars=value_cols,
        var_name=['지역', '성별', '연령', '항목'],  # type: ignore[arg-type]
        value_name='값',
    )

    long_df = long_df.rename(columns={YEAR_COLUMN: '시점'})
    long_df['시점'] = pd.to_numeric(long_df['시점'], errors='coerce')
    long_df['값'] = pd.to_numeric(long_df['값'], errors='coerce')
    long_df = long_df.dropna(subset=['시점', '값'])
    long_df['시점'] = long_df['시점'].astype(int)
    return long_df


def build_statistics(long_df: pd.DataFrame):
    """Build required tables for the assignment."""
    filtered = long_df[long_df['시점'] >= 2015].copy()
    filtered = filtered.drop(columns=['지역'])
    filtered = filtered[filtered['성별'].isin(['남자', '여자'])]

    gender_year = filtered[filtered['연령'] == '합계'].pivot_table(
        index='성별',
        columns='시점',
        values='값',
        aggfunc='sum',
    )

    age_year = filtered[filtered['연령'] != '합계'].pivot_table(
        index='연령',
        columns='시점',
        values='값',
        aggfunc='sum',
    )

    gender_age_year = filtered[filtered['연령'] != '합계'].pivot_table(
        index=['성별', '연령'],
        columns='시점',
        values='값',
        aggfunc='sum',
    )
    return gender_year, age_year, gender_age_year


def plot_gender_age_trends(gender_age_year: pd.DataFrame) -> None:
    """Plot yearly trends by sex and age."""
    plt.figure(figsize=(12, 6))
    x_values = gender_age_year.columns.to_list()
    for index_value in gender_age_year.index:
        row = gender_age_year.loc[index_value]
        y_values = pd.to_numeric(row, errors='coerce').fillna(0).to_numpy()

        if isinstance(index_value, tuple) and len(index_value) == 2:
            sex, age = index_value
            label_text = f'{sex}-{age}'
        else:
            label_text = str(index_value)

        plt.plot(
            x_values,
            y_values,
            marker='o',
            linewidth=1,
            label=label_text,
        )

    plt.xlabel('연도')
    plt.ylabel('일반가구원 수')
    plt.title('2015년 이후 연도별 남녀 연령별 일반가구원 추이')
    plt.xticks(gender_age_year.columns, rotation=45)
    plt.legend(title='성별-연령', ncol=2, fontsize=8)
    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=150)
    plt.show()


def main() -> None:
    plt.rcParams['font.family'] = ['Malgun Gothic', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    raw_df = load_dataframe()
    long_df = prepare_long_dataframe(raw_df)
    gender_year, age_year, gender_age_year = build_statistics(long_df)

    print('=== 성별 연도별 일반가구원 (2015년 이후) ===')
    print(gender_year)

    print('\n=== 연령별 연도별 일반가구원 (2015년 이후, 남녀 합산) ===')
    print(age_year)

    print('\n=== 성별/연령별 연도별 일반가구원 (2015년 이후) ===')
    print(gender_age_year)

    plot_gender_age_trends(gender_age_year)
    print(f'\n그래프 저장 완료: {PLOT_PATH}')


if __name__ == '__main__':
    main()