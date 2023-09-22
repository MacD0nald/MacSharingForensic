import os
from openpyxl import Workbook
import getpass
from datetime import datetime

# 스크립트 파일이 있는 디렉토리를 기준으로 대상 폴더를 설정합니다.
script_directory = os.path.dirname(__file__)

# 사용자 이름 가져오기
current_user = getpass.getuser()

target_folder = os.path.expanduser(f"~/Pictures/Photos Library.photoslibrary/originals")

# 엑셀 워크북 생성
workbook = Workbook()
sheet = workbook.active
sheet.title = 'photos_info'

# 대상 폴더 내의 폴더들을 반복
for root, dirs, files in os.walk(target_folder):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        file_stat = os.stat(file_path)
        
        # 폴더 경로를 엑셀에 추가
        folder_name = os.path.basename(root)
        
        # 파일 속성 정보를 엑셀에 추가
        sheet.append([folder_name, file_name, file_stat.st_size, file_stat.st_ctime, file_stat.st_mtime, file_stat.st_atime])

# 새로운 엑셀 파일을 만들기 위한 빈 리스트 생성
new_rows = []

# 시간 열의 유닉스 타임스탬프 값을 '0000년 00월 00일 00시 00분 00초' 형식으로 변경
for row in sheet.iter_rows(min_row=2, values_only=True):
    new_row = list(row)  # 튜플을 리스트로 변환하여 수정 가능한 리스트 생성
    for col_idx in range(4, 7):  # 4번째, 5번째, 6번째 열을 수정
        unix_timestamp = new_row[col_idx - 1]  # 열의 위치에 따라 인덱스 조정
        formatted_time = datetime.utcfromtimestamp(unix_timestamp).strftime('%Y년 %m월 %d일 %H시 %M분 %S초')
        new_row[col_idx - 1] = formatted_time  # 열의 위치에 따라 인덱스 조정
    new_rows.append(new_row)

# 새로운 엑셀 시트를 만들어 데이터 쓰기
new_sheet = workbook.create_sheet(title='새로운_시트_이름', index=0)  # 새로운 시트 생성
new_sheet.title = 'photos_info'
# 열 제목 추가
new_sheet.append(['폴더명', '파일명', '파일 크기 (바이트)', '생성 시간', '최근 수정 시간', '최근 접근 시간'])

for new_row in new_rows:
    new_sheet.append(new_row)  # 데이터 추가
    
# 기존 시트 제거 (선택사항)
workbook.remove(sheet)

# 변경된 내용을 엑셀 파일에 저장
excel_file_name = os.path.join(script_directory, 'photos_속성_정보.xlsx')
workbook.save(excel_file_name)

print('엑셀 파일이 저장되었습니다.')
