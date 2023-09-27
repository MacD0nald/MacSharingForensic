#Document version
# spotlight
import xml.etree.ElementTree as elemTree
import getpass
import os
import pandas as pd
import time

def make_copy(now, D_path):
    if not(os.path.isdir("Copy_Terminal")):
        os.mkdir("Copy_Terminal")
    os.chdir(D_path)
    if os.path.exists(".bash_history"):
        com = "cp .bash_history "+now+"/Copy_Terminal/.bash_history"
        os.popen(com)
    if os.path.exists(".zsh_history"):
        com = "cp .zsh_history "+now+"/Copy_Terminal/.zsh_history"
        os.popen(com)
    time.sleep(1)
    os.chdir(now)

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
now = os.getcwd() #현재 실행 경로
D_path = "/Users/"+current_user+"/"
#/Users/woobeenpark/Library/Application Support/com.apple.spotlight/com.apple.spotlight.Shortcuts.v3
col = ["Command", "Shell"]
terminal_history = []
try:
    make_copy(now, D_path)
    terminal_history = Command_history()
    df = pd.DataFrame(terminal_history, columns=col)
    os.chdir(now)
    df.to_csv("./CSV_Terminal.csv", sep=',')
except FileNotFoundError:
    print("This is invalid account name. Try again.")