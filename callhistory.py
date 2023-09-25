import sqlite3
from datetime import datetime
import shutil
import os
from openpyxl import Workbook
import getpass

# 파일 카피 불가
# sudo를 사용해도 permission denied가 뜸
# 한번 돌려봐 주세요...ㅠㅠㅠ 제 컴터가 문제가 아니길 바라면서도 돌아가길 바랍니다....

def directory():
    # 스크립트 파일이 있는 디렉토리를 기준으로 대상 폴더를 설정합니다.
    script_directory = os.path.dirname(__file__)

    # 사용자 이름 가져오기
    current_user = getpass.getuser()

    target_file = os.path.expanduser(f"~/Library/Application\ Support/CallHistoryDB/CallHistory.storedata-wal")
    
    # 새로 생성할 폴더 이름
    new_folder_name = 'destination_folder'

    # 현재 스크립트 파일이 있는 폴더 경로
    script_folder = os.path.dirname(os.path.abspath(__file__))

    # 새로운 폴더 생성
    new_folder_path = os.path.join(script_folder, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)

    # 파일 복사 (sudo를 사용하여 파일 복사)
    os.system(f"cp {target_file} {new_folder_path}")

# 스크립트 실행
directory()
