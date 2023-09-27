# spotlight
import xml.etree.ElementTree as elemTree
import getpass
import os
import pandas as pd
import time

def make_copy(script_folder, D_path):
    script_folder = os.path.dirname(os.path.abspath(__file__))
    Copy_folder = os.path.join(script_folder, 'Copy_Spotlight')
    if not(os.path.isdir(Copy_folder)):
        os.mkdir(Copy_folder)
    os.chdir(D_path)
    com = "cp com.apple.spotlight.Shortcuts.v3 "+os.path.join(Copy_folder, 'com.apple.spotlight.Shortcuts.v3')
    os.popen(com)
    time.sleep(1)
    os.chdir(script_folder)

def Spotlight_analyzer(Spotligjt_info):
    tree = elemTree.parse(os.path.join(script_folder, 'Copy_Spotlight/com.apple.spotlight.Shortcuts.v3'))

    root = tree.find("dict")
    for i in range(0, len(root), 2): 
        """print("사용자 검색 단어: ", root[i].text) #사용자 검색 단어
        print(root[i+1][0].text, ":",  root[i+1][1].text) #사용자 선택 프로그램
        print(root[i+1][2].text, ":",  root[i+1][3].text) # 사용자 마지막 사용 시간
        print("Path", ":",  root[i+1][5].text) #해당 어플리케이션 및 파일 경로
        print("---")"""
        Spotligjt_info.append([root[i+1][3].text, root[i].text, root[i+1][1].text,  root[i+1][5].text])
    return Spotligjt_info


D_path =os.path.expanduser(f"~/Library/Application Support/com.apple.spotlight/")
#/Users/woobeenpark/Library/Application Support/com.apple.spotlight/com.apple.spotlight.Shortcuts.v3
col = ["Last Used", "Search Keyword", "Search Result", "Search Result Path"]
Spotligjt_info = []

# 현재 스크립트 파일이 있는 폴더 경로
script_folder = os.path.dirname(os.path.abspath(__file__))

try:
    make_copy(script_folder, D_path)
    Spotlight_info = Spotlight_analyzer(Spotligjt_info)
    df = pd.DataFrame(Spotlight_info, columns=col)
    os.chdir(script_folder)
    # CSV 파일로 저장
    csv_file = os.path.join(script_folder, 'CSV_Spotlight.csv')  # CSV 파일 경로 설정
    df.to_csv(csv_file, sep=',')
except FileNotFoundError:
    print("This is invalid account name. Try again.")
