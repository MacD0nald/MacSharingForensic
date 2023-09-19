import xattr
import os
import datetime
import plistlib
import pandas as pd

def Check_Airdrop(path, data):
    for fname in os.listdir(path):
        os.chdir(path)
        x = xattr.listxattr(fname)
        x_list = xattr.xattr(fname)
        WhereFroms = b''
        quarantine = []
        content_flag = False
        Airdrop_flag = False
        for i in x: #('com.apple.metadata:kMDItemWhereFroms', 'com.apple.quarantine')
            if "kMDItemWhereFroms" in i:
                for j in x_list.items():
                    if "kMDItemWhereFroms" in j[0]:
                        content_flag = True
                        WhereFroms = j[1]
                        WhereFroms_bp = plistlib.loads(WhereFroms)
                        for k in WhereFroms_bp:
                            if not("http" in k):
                                Airdrop_flag = True
                                WhereFroms_device = k # Airdrop 보낸 기기명
            elif "com.apple.quarantine" in i:
                for j in x_list.items():
                    if "com.apple.quarantine" in j[0]:
                        content_flag = True
                        quarantine = j[1].split(b";")
                        #[0] = flag, [1] = timestamp, [2] = agent name - sharingd, [3] = UUID
                        if quarantine[2] == b"sharingd":
                            quarantine[2] = "Airdrop"
                            Airdrop_flag = True
                            unixtime_int = int(quarantine[1].decode(), 16)
                            quarantine[1] = datetime.datetime.fromtimestamp(unixtime_int).strftime('%Y-%m-%d %H:%M:%S')
        if content_flag == False:
            pass
        if Airdrop_flag == True:
            if len(quarantine) >3:
                data.append([fname, WhereFroms_device, quarantine[1], quarantine[2], quarantine[3].decode()])
            else:
                data.appenddata.append([fname, WhereFroms_device, quarantine[1], quarantine[2], "NA"])
            Airdrop_flag = False
        else:
            pass
    return data

username = input("Input the Username: ") # Username 입력
now = os.getcwd()
D_path = "/Users/"+username+"/Downloads"
col = ["file_name", "SenderName", "Timestamp", "AgentName", "Quarantine_UUID"]
Airdrop_info = []
try:
    Airdrop_info = Check_Airdrop(D_path, Airdrop_info)
    df = pd.DataFrame(Airdrop_info, columns=col)
    print(df)
    os.chdir(now)
    if not(os.path.isdir("./Result")):
        os.mkdir("Result")
        df.to_csv("./Result/AirDrop.csv", sep=',')
    else:
        df.to_csv("./Result/AirDrop.csv", sep=',')
except FileNotFoundError:
    print("This is invalid account name. Try again.")