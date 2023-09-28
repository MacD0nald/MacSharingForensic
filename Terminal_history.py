#Document version
# spotlight
import xml.etree.ElementTree as elemTree
import getpass
import os
import pandas as pd
import time

def make_copy(now, D_path):
    script_folder = os.path.dirname(os.path.abspath(__file__))
    Copy_folder = os.path.join(script_folder, 'Copy_Terminal')
    if not(os.path.isdir(Copy_folder)):
        os.mkdir(os.path.join(script_folder, 'Copy_Terminal'))
    os.chdir(D_path)
    if os.path.exists(".bash_history"):
        com = "cp .bash_history "+os.path.join(Copy_folder, 'bash_history')
        os.popen(com)
    if os.path.exists(".zsh_history"):
        com = "cp .zsh_history "+os.path.join(Copy_folder, 'zsh_history')
        os.popen(com)
    time.sleep(1)
    os.chdir(script_folder)

def Command_history():
    os.chdir("./Copy_Terminal/")
    terminal_history = []
    for i in os.listdir():
        with open(i, "rb") as f:
            if "zsh" in i:
                for j in f.readlines():
                    terminal_history.append([str(j), "zsh_shell"])
            if "bash" in i:
                for j in f.readlines():
                    terminal_history.append([str(j), "bash_shell"])
    return terminal_history

current_user = getpass.getuser() # Username
D_path = os.path.expanduser(f"~/")
col = ["Command", "Shell"]
terminal_history = []

# 현재 스크립트 파일이 있는 폴더 경로
script_folder = os.path.dirname(os.path.abspath(__file__))

try:
    make_copy(script_folder, D_path)
    terminal_history = Command_history()
    df = pd.DataFrame(terminal_history, columns=col)
    os.chdir(script_folder)
    # CSV 파일로 저장
    csv_file = os.path.join(script_folder, 'CSV_Terminal.csv')  # CSV 파일 경로 설정
    df.to_csv(csv_file, sep=',')
except FileNotFoundError:
    print("This is invalid account name. Try again.")
