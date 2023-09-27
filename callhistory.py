import sqlite3
import datetime
import csv
import os
import getpass
import shutil

def directory():
    # 스크립트 파일이 있는 디렉토리를 기준으로 대상 폴더를 설정합니다.
    script_directory = os.path.dirname(__file__)

    # 사용자 이름 가져오기
    current_user = getpass.getuser()

    target_folder = os.path.expanduser(f"~/Library/Application Support/CallHistoryDB")
    target_files = os.listdir(target_folder)
    

    # 현재 스크립트 파일이 있는 폴더 경로
    script_folder = os.path.dirname(os.path.abspath(__file__))

    # 모든 파일을 복사하여 대상 폴더로 붙여넣기
    for file in target_files:
        source_file_path = os.path.join(target_folder, file)
        destination_file_path = os.path.join(script_folder, file)
        
        # 파일을 복사하여 붙여넣기
        try:
            shutil.copy2(source_file_path, destination_file_path)
            print(f'파일 복사 완료: {file}')
        except Exception as e:
            print(f'파일 복사 실패: {file}, 오류: {str(e)}')

directory()

def convert_coretime_to_readable(timestamp):
     # Mac Absolute Time (CoreServices Timestamp)는 2001년 1월 1일 기준
    base_date = datetime.datetime(2001, 1, 1)

    # timedelta 객체를 사용해 초를 추가
    dt_object = base_date + datetime.timedelta(seconds=timestamp)

    # 원하는 포맷으로 datetime 객체를 문자열로 변환
    readable_time = dt_object.strftime('%Y-%m-%d %H:%M:%S') + " (UTC+0)"
    return readable_time

conn = sqlite3.connect("CallHistory.storedata")
cursor = conn.cursor()

# CSV 파일 저장 경로
csv_file = 'output.csv'

# 특정 테이블 선택
table_name = 'ZCALLRECORD'
columns_to_read = ['ZADDRESS', 'ZISO_COUNTRY_CODE', 'ZDATE', 'ZDURATION']

# SQL 쿼리 작성 (특정 테이블의 특정 열 읽기)
query = f"SELECT {', '.join(columns_to_read)} FROM {table_name}"

# 쿼리 실행
cursor.execute(query)

# 결과 가져오기
rows = cursor.fetchall()

# 결과 가져오기
results = cursor.fetchall()


# CSV 파일로 저장
with open(csv_file, 'w', newline='') as csv_output:
    csv_writer = csv.writer(csv_output)
    
    # 열 이름을 CSV 파일의 첫 행으로 쓰기
    csv_writer.writerow(columns_to_read)
    
    for row in results:
        # 타임스탬프 열의 값을 보기 좋은 형식으로 변환
        timestamp_index = columns_to_read.index('ZDATE')
        timestamp = row[timestamp_index]
        formatted_timestamp = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        # 타임스탬프 열의 값을 보기 좋은 형식으로 교체
        row = list(row)
        row[timestamp_index] = formatted_timestamp
        
        # 결과 행을 CSV 파일에 쓰기
        csv_writer.writerow(row)


print(f"데이터를 {csv_file}로 저장했습니다.")


# 연결 종료
conn.close()
