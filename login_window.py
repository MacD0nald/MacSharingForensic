import os
import time
import plistlib
import csv
import getpass

def makecopy():
  if os.path.isdir('./Copy_LoginWindow')==False:
    os.mkdir('./Copy_LoginWindow)')
  now = os.getcwd()+'/Copy_LoginWindow)'

  path = "/Library/Preferences"
  os.chdir(path)

  com = "cp com.apple.loginwindow.plist "+ now +"/"+"com.apple.loginwindow.plist"
  os.popen(com)
  time.sleep(3)
  os.chdir(now)

def recursive_extract(data, parent_key='', results=None):
    if results is None:
        results = []

    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, (dict, list)):
                recursive_extract(v, new_key, results)
            else:
                results.append(f"{new_key}: {v}")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            new_key = f"{parent_key}[{idx}]"
            if isinstance(item, (dict, list)):
                recursive_extract(item, new_key, results)
            else:
                results.append(f"{new_key}: {item}")
    return results

def plist_to_txt (input_data, file_name):
  with open(input_data, 'rb') as f:
    plist_data = input_data.load(f)
  
  extracted_data = recursive_extract(plist_data)

  with open (file_name, 'w')as f:
    for line in extracted_data:
      f.write(line + 'Wn')

now = os.getcwd()

makecopy()

input_data = now+"/Copy_LoginWindow/com.apple.loginwindow.plist"
file_name = now+"/"+"LoginWinow.txt"
plist_to_txt(input_data, file_name)
