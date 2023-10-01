# spotlight
import xml.etree.ElementTree as elemTree
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

def Spotlight_analyzer(Spotlight_info):
    # 현재 스크립트 파일이 있는 폴더 경로
    script_folder = os.path.dirname(os.path.abspath(__file__))
    tree = elemTree.parse(os.path.join(script_folder, 'Copy_Spotlight/com.apple.spotlight.Shortcuts.v3'))

    root = tree.find("dict")
    for i in range(0, len(root), 2): 
        app_name = ''
        last_used = ''
        path = ''
        for j in range(0, len(root[i+1])):
            if root[i+1][j].text == "DISPLAY_NAME":
                app_name = root[i+1][j+1].text
            elif root[i+1][j].text == "LAST_USED":
                last_used = root[i+1][j+1].text
            elif root[i+1][j].text == "URL":
                path = root[i+1][j+1].text
        Spotlight_info.append([last_used, root[i].text, app_name,  path])
    return Spotlight_info

def Spotlight():
    D_path =os.path.expanduser(f"~/Library/Application Support/com.apple.spotlight/")
    col = ["Last Used", "Search Keyword", "Search Result", "Search Result Path"]
    Spotlight_info = []
    
    # 현재 스크립트 파일이 있는 폴더 경로
    script_folder = os.path.dirname(os.path.abspath(__file__))
    
    make_copy(script_folder, D_path)
    Spotlight_info = Spotlight_analyzer(Spotlight_info)
    if Spotlight_info is not None : 
        df = pd.DataFrame(Spotlight_info, columns=col)
        os.chdir(script_folder)
        # CSV 파일로 저장
        csv_file = os.path.join(script_folder, 'CSV_Spotlight.csv')  # CSV 파일 경로 설정
        df.to_csv(csv_file, sep=',')
        print("Spotlight output :", csv_file)
