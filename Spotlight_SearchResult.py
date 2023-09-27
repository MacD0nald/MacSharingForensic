# spotlight
import xml.etree.ElementTree as elemTree
import getpass
import os
import pandas as pd
import time

def make_copy(now, D_path):
    if not(os.path.isdir("Copy_Spotlight")):
        os.mkdir("Copy_Spotlight")
    os.chdir(D_path)
    com = "cp com.apple.spotlight.Shortcuts.v3 "+now+"/Copy_Spotlight/com.apple.spotlight.Shortcuts.v3"
    os.popen(com)
    time.sleep(1)
    os.chdir(now)

def Spotlighg_analyzer(Spotligjt_info):
    tree = elemTree.parse('./Copy_Spotlight/com.apple.spotlight.Shortcuts.v3')

    root = tree.find("dict")
    for i in range(0, len(root), 2): 
        """print("사용자 검색 단어: ", root[i].text) #사용자 검색 단어
        print(root[i+1][0].text, ":",  root[i+1][1].text) #사용자 선택 프로그램
        print(root[i+1][2].text, ":",  root[i+1][3].text) # 사용자 마지막 사용 시간
        print("Path", ":",  root[i+1][5].text) #해당 어플리케이션 및 파일 경로
        print("---")"""
        Spotligjt_info.append([root[i+1][3].text, root[i].text, root[i+1][1].text,  root[i+1][5].text])
    return Spotligjt_info


current_user = getpass.getuser() # Username
now = os.getcwd() #현재 실행 경로
D_path = "/Users/"+current_user+"/Library/Application Support/com.apple.spotlight/"
#/Users/woobeenpark/Library/Application Support/com.apple.spotlight/com.apple.spotlight.Shortcuts.v3
col = ["Last Used", "Search Keyword", "Search Result", "Search Result Path"]
Spotligjt_info = []
try:
    make_copy(now, D_path)
    Spotligjt_info = Spotlighg_analyzer(Spotligjt_info)
    df = pd.DataFrame(Spotligjt_info, columns=col)
    os.chdir(now)
    df.to_csv("./CSV_Spotlight.csv", sep=',')
except FileNotFoundError:
    print("This is invalid account name. Try again.")