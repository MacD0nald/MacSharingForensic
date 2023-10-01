import plistlib
import csv
import os
import time

def makecopy():
  if os.path.isdir('./Copy_LoginWindow')==False:
    os.mkdir('./Copy_LoginWindow')
  now = os.getcwd()+'/Copy_LoginWindow'

  path = "/Library/Preferences"
  os.chdir(path)

  com = "cp com.apple.loginwindow.plist "+ now +"/"+"com.apple.loginwindow.plist"
  os.popen(com)
  time.sleep(3)
  os.chdir(now)

def traverse_dict(d, path=[]):
    rows = []
    for k, v in d.items():
        current_path = path + [k]
        if isinstance(v, dict):
            rows.extend(traverse_dict(v, current_path))
        else:
            rows.append(current_path + [str(v)])
    return rows

def plist_to_csv_using_plistlib(plist_path):
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
    with open(now+"/LoginWindow.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Level 1", "Level 2", "Level 3"])
        writer.writerows(rows)
# 사용
now = os.getcwd()

makecopy()

input_data = now+"/Copy_LoginWindow/com.apple.loginwindow.plist"
plist_to_csv(input_data)
