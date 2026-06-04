# 문제3. 스마트팜의 시작

## 문제 요약
- 센서(온도/조도/습도) 데이터를 주기적으로 생성하고 MySQL DB에 저장하는 스마트팜 시뮬레이션 문제입니다.
- 저장된 데이터로 5분 평균 및 시간대별 온도 텍스트 그래프를 출력합니다.

## 핵심 파일
- `smart_farm_system.py`: 멀티스레드 센서 수집, 큐 기반 DB 저장, 통계 출력
- `parm_data.csv`, `smart_farm.db`: 예시 데이터 파일

## 풀이에 필요한 정보
1. 실행 전 MySQL 접속 정보(`--db-host`, `--db-user`, `--db-password`)를 맞춰야 합니다.
2. `initialize_database`가 DB/테이블(`parm_data`)을 자동 생성합니다.
3. 센서 스레드→큐→DB 워커 스레드 구조로 동작합니다.
4. 실행 예시: `python smart_farm_system.py --sensor-count 5 --interval 10 --runtime 65`
