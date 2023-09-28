import os
import plistlib
from datetime import datetime
import shutil
import csv

def directory():

    # 경로에 사용자 이름 추가
    source_folder = os.path.expanduser(f"~/Library/Application Support/AddressBook/Sources")

    current_script_directory = os.path.dirname(__file__)

    # 대상 폴더 경로 (현재 스크립트 파일이 있는 폴더로 상대 경로 지정)
    destination_folder = os.path.join(current_script_directory, "Copy_Contact")

    # 대상 폴더가 없다면 생성
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 원본 폴더에서 폴더 목록 가져오기
    files = os.listdir(source_folder)
    files.remove('.DS_Store')
    
    for i in files:
        source_folder2 = os.path.join(source_folder, i)
        source_folder2 = os.path.join(source_folder2, "Metadata")
        files = os.listdir(source_folder2)

        # 파일을 순회하면서 복사 및 이름 변경
        for i, filename in enumerate(files):
            if filename.endswith('.abcdp'):
                source_file_path = os.path.join(source_folder2, filename)
                # 복사한 파일을 대상 폴더에 저장
                new_filename = f'{i+1}.abcdp'
                destination_file_path = os.path.join(destination_folder, new_filename)
                shutil.copy(source_file_path, destination_file_path)
                # 확장자를 변경하기 위해 파일 이동
                new_extension = '.plist'
                renamed_file_path = os.path.join(destination_folder, f'{i+1}{new_extension}')
                os.rename(destination_file_path, renamed_file_path)
    return destination_folder

def read_bplist(file_path):
    with open(file_path, 'rb') as fp:
        plist_data = plistlib.load(fp)
    return plist_data

def sel_bplist(plist_data):
    desired_keys = ['First', 'Last', 'Organization', 'Creation', 'Modification']
    filtered_dict = {}

    for key in desired_keys:
        value = plist_data.get(key, '')
        filtered_dict[key] = value

    Phone_dict = plist_data.get('Phone', {})
    
    values = Phone_dict.get('values', [])
    
    filtered_dict['phone number'] = values[0] if values else None
    
    for key in ['Creation', 'Modification']:
        if key in filtered_dict:
            creation_datetime = filtered_dict[key]
            formatted_creation = creation_datetime.strftime('%Y년 %m월 %d일 %H시 %M분 %S.%f초')
            filtered_dict[key] = formatted_creation
    return filtered_dict


if __name__ == "__main__":
    destination_folder = directory()
    all_filtered_data = []

    for filename in os.listdir(destination_folder):
        if filename.endswith(".plist"):
            file_path = os.path.join(destination_folder, filename)
            
            plist_data = read_bplist(file_path)
            
            filtered_data = sel_bplist(plist_data)
            all_filtered_data.append(filtered_data)

    # Specify the CSV file path
    current_script_directory = os.path.dirname(__file__)
    csv_file_path = os.path.join(current_script_directory, 'CSV_Contact.csv')  # Change the file extension to .csv

    # Open the CSV file in write mode
    with open(csv_file_path, 'w', newline='') as csv_file:
        # Create a CSV writer
        csv_writer = csv.DictWriter(csv_file, fieldnames=all_filtered_data[0].keys())

        # Write the header row
        csv_writer.writeheader()

        # Write the data rows
        csv_writer.writerows(all_filtered_data)
