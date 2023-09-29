import os
from openpyxl import Workbook
import getpass
from datetime import datetime

import os
import csv
if __name__ == "__main__":
    # 현재 스크립트 파일이 있는 디렉토리를 얻습니다.
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # CSV 파일에 저장할 헤더를 정의합니다.
    csv_header = ['폴더명', '파일명', '파일 크기 (바이트)', '생성 시간', '최종 수정 시간']
    
    # 사용자 이름 가져오기
    current_user = getpass.getuser()
    target_folder_path = os.path.expanduser(f"~/Pictures/Photos Library.photoslibrary/originals")
    
    # CSV 파일을 열고 헤더를 쓰기 모드로 씁니다.
    csv_file_path = os.path.join(script_directory, 'file_attributes.csv')
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_header)
    
        # 0부터 F까지의 폴더를 순회합니다.
        for folder_name in range(16):
            folder_name = format(folder_name, 'X')  # 16진수로 변환 (0-F)
            folder_path = os.path.join(target_folder_path, folder_name)  # 실제 폴더 경로로 변경해야 합니다.
    
            # 폴더 내의 파일 리스트를 가져옵니다.
            file_list = os.listdir(folder_path)
    
            # 파일 정보를 읽어서 CSV 파일에 씁니다.
            for file_name in file_list:
                file_path = os.path.join(folder_path, file_name)
                file_size = os.path.getsize(file_path)
                file_create_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                file_modify_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    
                # CSV 파일에 데이터를 씁니다.
                writer.writerow([folder_name, file_name, file_size, file_create_time, file_modify_time])
    
    
                # CSV 파일에 데이터를 씁니다.
                writer.writerow([folder_name, file_name, file_size, file_create_time, file_modify_time])
    
    print(f'CSV 파일이 {csv_file_path} 경로에 생성되었습니다.')
