import argparse
import queue
import random
import threading
import time
from collections import defaultdict
from datetime import datetime

import mysql.connector
from mysql.connector import Error


class ParmSensor:  # noqa: E302
    """스마트 팜 센서 1개를 표현하는 클래스."""

    def __init__(self, name):
        self.name = name
        self.Temperature = 0
        self.Illuminance = 0
        self.Humidity = 0
        self.SetData()

    def SetData(self):
        """요구 범위 내 랜덤 값으로 온도/조도/습도를 갱신한다."""
        self.Temperature = random.randint(20, 30)
        self.Illuminance = random.randint(5000, 10000)
        self.Humidity = random.randint(40, 70)

    def GetData(self):
        """현재 센서 값을 튜플로 반환한다."""
        return self.Temperature, self.Illuminance, self.Humidity


def get_connection(db_config, use_database=True):
    """MySQL 연결 객체를 반환한다."""
    config = {
        'host': db_config['host'],
        'port': db_config['port'],
        'user': db_config['user'],
        'password': db_config['password'],
    }
    if use_database:
        config['database'] = db_config['database']
    return mysql.connector.connect(**config)


def initialize_database(db_config):
    """MySQL 데이터베이스 및 parm_data 테이블을 생성한다."""
    db_name = db_config['database']
    create_database_query = f'CREATE DATABASE IF NOT EXISTS {db_name}'
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS parm_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            input_time DATETIME NOT NULL,
            sensor_name VARCHAR(20) NOT NULL,
            temperature INT NOT NULL,
            illuminance INT NOT NULL,
            humidity INT NOT NULL
        )
    '''

    connection = None
    cursor = None

    try:
        connection = get_connection(db_config, use_database=False)
        cursor = connection.cursor()
        cursor.execute(create_database_query)
        connection.commit()

        cursor.close()
        connection.close()

        connection = get_connection(db_config, use_database=True)
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def insert_sensor_data(
    connection,
    input_time,
    sensor_name,
    temperature,
    illuminance,
    humidity,
):
    """센서 1건 데이터를 parm_data 테이블에 저장한다."""
    query = '''
        INSERT INTO parm_data (
            input_time,
            sensor_name,
            temperature,
            illuminance,
            humidity
        )
        VALUES (%s, %s, %s, %s, %s)
    '''

    cursor = connection.cursor()
    try:
        cursor.execute(
            query,
            (input_time, sensor_name, temperature, illuminance, humidity),
        )
        connection.commit()
    finally:
        cursor.close()


def get_sensor_data(db_config):
    """parm_data 테이블 전체 데이터를 시간순으로 반환한다."""
    query = '''
        SELECT id, input_time, sensor_name, temperature, illuminance, humidity
        FROM parm_data
        ORDER BY input_time, id
    '''

    connection = None
    cursor = None
    try:
        connection = get_connection(db_config, use_database=True)
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def print_five_minute_average(records):
    """메모리 내 레코드 기준 5분 버킷 평균을 출력한다."""
    grouped = defaultdict(
        lambda: {'temp': 0, 'light': 0, 'humi': 0, 'count': 0}
    )

    for row in records:
        dt = datetime.strptime(row['input_time'], '%Y-%m-%d %H:%M:%S')
        minute_bucket = (dt.minute // 5) * 5
        bucket_dt = dt.replace(minute=minute_bucket, second=0)
        key = (row['sensor_name'], bucket_dt.strftime('%Y-%m-%d %H:%M:00'))

        grouped[key]['temp'] += row['temperature']
        grouped[key]['light'] += row['illuminance']
        grouped[key]['humi'] += row['humidity']
        grouped[key]['count'] += 1

    if not grouped:
        print('5분 평균 데이터가 없습니다.')
        return

    print('\n[5분 단위 평균 출력]')
    for key in sorted(grouped.keys()):
        sensor_name, bucket_time = key
        agg = grouped[key]
        count = agg['count']
        avg_temp = agg['temp'] / count
        avg_light = agg['light'] / count
        avg_humi = agg['humi'] / count
        print(
            f'{bucket_time} {sensor_name} -> '
            f'temp {avg_temp:.2f}, light {avg_light:.2f}, '
            f'humi {avg_humi:.2f} (n = {count})'
        )


def print_hourly_temperature_graph(rows):
    """센서별 시간대 평균 온도를 텍스트 그래프로 출력한다."""
    grouped = defaultdict(lambda: {'sum_temp': 0, 'count': 0, 'max_humi': 0})

    for _id, input_time, sensor_name, temperature, _illuminance, humidity in rows:
        if isinstance(input_time, str):
            dt = datetime.strptime(input_time, '%Y-%m-%d %H:%M:%S')
        else:
            dt = input_time
        hour_bucket = dt.strftime('%Y-%m-%d %H:00:00')
        key = (sensor_name, hour_bucket)
        grouped[key]['sum_temp'] += temperature
        grouped[key]['count'] += 1
        grouped[key]['max_humi'] = max(grouped[key]['max_humi'], humidity)

    if not grouped:
        print('\n[시간대별 평균 온도 그래프] 데이터가 없습니다.')
        return

    print('\n[시간대별 평균 온도 그래프]')
    for sensor_name, hour_bucket in sorted(grouped.keys()):
        item = grouped[(sensor_name, hour_bucket)]
        avg_temp = item['sum_temp'] / item['count']
        bar = '#' * int(round(avg_temp))
        hot_point = ''
        if item['max_humi'] > 90:
            hot_point = ' \033[91m*HUMI>90\033[0m'
        print(f'{hour_bucket} {sensor_name:6s} | {bar} ({avg_temp:.2f}){hot_point}')


def sensor_task(
    sensor, sensorQ, records, records_lock, stop_event, interval_seconds
):
    """센서 데이터를 생성하고 출력한 뒤, FIFO 큐에 넣는다."""
    while not stop_event.is_set():
        sensor.SetData()
        temperature, illuminance, humidity = sensor.GetData()
        now_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(
            f'{now_text} {sensor.name} - '
            f'temp {temperature:02d}, light {illuminance:05d}, '
            f'humi {humidity:02d}'
        )

        payload = {
            'input_time': now_text,
            'sensor_name': sensor.name,
            'temperature': temperature,
            'illuminance': illuminance,
            'humidity': humidity,
        }
        sensorQ.put(payload)

        with records_lock:
            records.append(payload)

        if stop_event.wait(interval_seconds):
            break


def db_worker_task(db_config, sensorQ, stop_event):
    """1초마다 큐를 확인하고 데이터가 있으면 DB에 저장한다."""
    connection = None
    try:
        connection = get_connection(db_config, use_database=True)
    except Error as err:
        print(f'MySQL 연결 실패: {err}')
        return

    while not stop_event.is_set() or not sensorQ.empty():
        try:
            payload = sensorQ.get(timeout=1)
        except queue.Empty:
            continue

        try:
            insert_sensor_data(
                connection=connection,
                input_time=payload['input_time'],
                sensor_name=payload['sensor_name'],
                temperature=payload['temperature'],
                illuminance=payload['illuminance'],
                humidity=payload['humidity'],
            )
        except Error as err:
            print(f'DB 저장 실패: {err}')
        sensorQ.task_done()

    if connection is not None and connection.is_connected():
        connection.close()


def build_sensors(sensor_count):
    """Parm-1 ~ Parm-n 센서 객체 리스트를 만든다."""
    sensors = []
    for index in range(1, sensor_count + 1):
        sensors.append(ParmSensor(f'Parm-{index}'))
    return sensors


def run_system(db_config, sensor_count, interval_seconds, runtime_seconds):
    """스마트 팜 센서/큐/DB 저장 시스템을 실행한다."""
    try:
        initialize_database(db_config)
    except Error as err:
        print(f'MySQL 초기화 실패: {err}')
        return

    sensorQ = queue.Queue()
    stop_event = threading.Event()
    records = []
    records_lock = threading.Lock()

    sensors = build_sensors(sensor_count)
    threads = []

    db_thread = threading.Thread(
        target=db_worker_task,
        args=(db_config, sensorQ, stop_event),
        name='db-worker',
        daemon=True,
    )
    db_thread.start()
    threads.append(db_thread)

    for sensor in sensors:
        thread = threading.Thread(
            target=sensor_task,
            args=(
                sensor,
                sensorQ,
                records,
                records_lock,
                stop_event,
                interval_seconds,
            ),
            name=f'{sensor.name}-thread',
            daemon=True,
        )
        thread.start()
        threads.append(thread)

    start_time = time.time()

    try:
        while True:
            elapsed = time.time() - start_time
            if runtime_seconds > 0 and elapsed >= runtime_seconds:
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print('\n사용자 중단 요청으로 종료합니다.')

    stop_event.set()

    for thread in threads:
        thread.join(timeout=3)

    rows = get_sensor_data(db_config)
    print(f'\nDB 저장 완료 건수: {len(rows)}')

    with records_lock:
        copied_records = list(records)
    print_five_minute_average(copied_records)
    print_hourly_temperature_graph(rows)


def parse_arguments():
    """실행 인자를 파싱한다."""
    parser = argparse.ArgumentParser(description='Smart Parm Sensor System')
    parser.add_argument('--db-host', default='127.0.0.1', help='MySQL 호스트')
    parser.add_argument('--db-port', type=int, default=3306, help='MySQL 포트')
    parser.add_argument('--db-user', default='root', help='MySQL 사용자')
    parser.add_argument('--db-password', default='', help='MySQL 비밀번호')
    parser.add_argument(
        '--db-name',
        default='smart_farm',
        help='MySQL 데이터베이스 이름',
    )
    parser.add_argument('--sensor-count', type=int, default=5, help='센서 개수')
    parser.add_argument('--interval', type=int, default=10, help='센서 수집 주기(초)')
    parser.add_argument(
        '--runtime',
        type=int,
        default=65,
        help='전체 실행 시간(초), 0 이하이면 무한 실행',
    )
    return parser.parse_args()


def main():
    """엔트리 포인트."""
    args = parse_arguments()
    db_config = {
        'host': args.db_host,
        'port': args.db_port,
        'user': args.db_user,
        'password': args.db_password,
        'database': args.db_name,
    }
    run_system(
        db_config=db_config,
        sensor_count=args.sensor_count,
        interval_seconds=args.interval,
        runtime_seconds=args.runtime,
    )


if __name__ == '__main__':
    main()