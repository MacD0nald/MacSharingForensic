import plistlib
import csv
import os
import time

def makecopy():
  if os.path.isdir('./Copy_LoginWindow')==False:
    os.mkdir('./Copy_LoginWindow')
  output_path = os.getcwd()+'/Copy_LoginWindow'
  now = os.getcwd()

  path = "/Library/Preferences"
  os.chdir(path)

  com = "cp com.apple.loginwindow.plist "+ output_path +"/"+"com.apple.loginwindow.plist"
  os.popen(com)
  time.sleep(3)
  os.chdir(now)

def traverse_dict(d, path=[]):
    rows = []
    for k, v in d.items():
        current_path = path + [k]
        if isinstance(v, dict):
            if len(current_path) == 2:  
                for key in v.keys():
                    rows.append(current_path + [key])
            else:
                rows.extend(traverse_dict(v, current_path))
        else:
            while len(current_path) < 3:
                current_path.append('')
            current_path[-1] = str(v)
            rows.append(current_path)
    return rows


def plist_to_csv(plist_path, file_name):
    # plist 파일 읽기
    with open(plist_path, 'rb') as f:
        pl = plistlib.load(f)

    rows = traverse_dict(pl)

    # 중복된 Level 1, Level 2 값을 빈 문자열로 대체
    prev_l1, prev_l2 = None, None
    for row in rows:
        l1, l2, _ = row
        if l1 == prev_l1:
            row[0] = ''
            if l2 == prev_l2:
                row[1] = ''
        prev_l1, prev_l2 = l1, l2

    # CSV 파일로 저장
    with open(file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Level 1", "Level 2", "Level 3"])
        writer.writerows(rows)

def login():
    now = os.getcwd()

    makecopy()

    input_data = now+"/Copy_LoginWindow/com.apple.loginwindow.plist"
    file_name = now+"/CSV_LoginWindow.csv"
    plist_to_csv(input_data, file_name)
    print(f"login window: {file_name}")
