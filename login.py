import csv
import xml.etree.ElementTree as ET
from io import StringIO
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

def extract_cell_data(parent_keys, element):
    rows = []
    if not parent_keys:  # 1차 dict일 때
        for i in range(0, len(element), 2):
            key = element[i].text
            if element[i+1].tag == 'dict':
                rows.extend(extract_cell_data(parent_keys + [key], element[i+1]))
            else:
                value = element[i+1].text if element[i+1].text else element[i+1].tag
                rows.append([key, '', value])
    elif len(parent_keys) == 1:  # 2차 dict일 때
        for i in range(0, len(element), 2):
            key = element[i].text
            if element[i+1].tag == 'dict':
                rows.extend(extract_cell_data(parent_keys + [key], element[i+1]))
            else:
                value = element[i+1].text if element[i+1].text else element[i+1].tag
                rows.append([parent_keys[0], key, value])
    else:  # 3차 dict일 때
        for i in range(0, len(element), 2):
            key = element[i].text
            value = element[i+1].text if element[i+1].text else element[i+1].tag
            rows.append(parent_keys + [key])

    return rows

def plist_to_csv(xml_data):
    root = ET.fromstring(xml_data)
    main_dict = root.find('dict')
    
    rows = extract_cell_data([], main_dict)

    # 중복 값을 처리하여 빈 문자열로 대체
    prev_l1, prev_l2 = None, None
    for row in rows:
        l1, l2, _ = row
        if l1 == prev_l1:
            row[0] = ''
            if l2 == prev_l2:
                row[1] = ''
        prev_l1, prev_l2 = l1, l2

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Level 1", "Level 2", "Level 3"])
    writer.writerows(rows)
    
    return output.getvalue()

# 사용
def login():
    now = os.getcwd()
  
    makecopy()
  
    input_data = now+"/Copy_LoginWindow/com.apple.loginwindow.plist"
    csv_result = plist_to_csv(input_data)
    
    file_name = now+"/"+"LoginWinow.csv"

    with open(file_name, "w") as f:
      f.write(csv_result)
