# 문제2. 그때 지구 그리고 한국에서는

## 문제 요약
- `korea_earth.csv`(KOSIS 형식 다중 헤더)에서 2015년 이후 일반가구원 데이터를 성별/연령별로 분석하는 문제입니다.
- 결과로 성별·연령별 표와 추이 그래프를 생성합니다.

## 핵심 파일
- `earth_and_korea.py`: CSV 로드, long format 변환, 피벗 통계, 선 그래프 저장
- `korea_earth.csv`: 원본 데이터(cp949 인코딩)
- `earth_korea_gender_age_trend.png`: 시각화 결과

## 풀이에 필요한 정보
1. CSV는 `header=[0,1,2,3]` 다중 컬럼으로 읽고 `일반가구원` 항목만 사용합니다.
2. `melt`로 long 형태로 바꾼 뒤 `시점>=2015` 필터를 적용합니다.
3. `pivot_table`로 성별/연령별 집계표를 만듭니다.
4. 실행: 해당 폴더에서 `python earth_and_korea.py`
