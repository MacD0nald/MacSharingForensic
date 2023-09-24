import xattr
import os
import datetime
import plistlib
import pandas as pd

def Check_Download(path, data):
    os.chdir(path)
    for fname in os.listdir(path):
        x = xattr.listxattr(fname)
        x_list = xattr.xattr(fname)
        WhereFroms = b''
        WhereFroms_bp = ''
        WhereFroms_device = ''
        WhereFroms_site = ''
        quarantine = []
        content_flag = False
        Airdrop_flag = False
        quan_flag = False
        dateAdded= os.path.getctime(fname)
        dateAdded = datetime.datetime.fromtimestamp(dateAdded).strftime('%Y-%m-%d %H:%M:%S')
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
                            else:
                                WhereFroms_site = WhereFroms_bp
            elif "com.apple.quarantine" in i:
                for j in x_list.items():
                    if "com.apple.quarantine" in j[0]:
                        quarantine = j[1].split(b";")
                        #[0] = flag, [1] = timestamp, [2] = agent name - sharingd, [3] = UUID
                        if quarantine[2] == b"sharingd":
                            Airdrop_flag = True
                            quarantine[2] = "Airdrop"
                            Airdrop_flag = True
                            unixtime_int = int(quarantine[1].decode(), 16)
                            quarantine[1] = datetime.datetime.fromtimestamp(unixtime_int).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            quan_flag = True
                            quarantine[2] = quarantine[2].decode()
                            unixtime_int = int(quarantine[1].decode(), 16)
                            quarantine[1] = datetime.datetime.fromtimestamp(unixtime_int).strftime('%Y-%m-%d %H:%M:%S')
        if content_flag == True:
            if Airdrop_flag == True:
                if len(quarantine) >3:
                    data.append([dateAdded, quarantine[1],fname, quarantine[2],WhereFroms_device,  quarantine[3].decode()])
                else:
                    data.append([dateAdded, quarantine[1],fname, quarantine[2],WhereFroms_device, ""])
                Airdrop_flag = False
            elif quan_flag:
                data.append([dateAdded, quarantine[1],fname, quarantine[2], WhereFroms_site, quarantine[3].decode()])
                quan_flag = False
            else:
                data.append([dateAdded, quarantine[1],fname, quarantine[2],WhereFroms_device, ""])
                content_flag = False
        if content_flag == False:
            if Airdrop_flag == True:
                if len(quarantine) >3:
                    data.append([dateAdded, quarantine[1],fname, WhereFroms_device, quarantine[2], quarantine[3].decode()])
                else:
                    data.append([dateAdded, quarantine[1],fname, quarantine[2],WhereFroms_device, ""])
                Airdrop_flag = False
            elif quan_flag:
                data.append([dateAdded, quarantine[1],fname, quarantine[2], "", quarantine[3].decode()])
                quan_flag = False
            else: 
                data.append([dateAdded, "", fname, "", "", ""])
    return data

username = input("Input the Username: ") # Username 입력
now = os.getcwd()
D_path = "/Users/"+username+"/Downloads"
col = ["Created Timestamp", "Download Timestamp", "file_name", "Downlaod Agent","Download Source", "Quarantine_UUID"]
Airdrop_info = []
try:
    Airdrop_info = Check_Download(D_path, Airdrop_info)
    df = pd.DataFrame(Airdrop_info, columns=col)
    print(df)
    os.chdir(now)
    if not(os.path.isdir("./Result")):
        os.mkdir("Result")
        df.to_csv("./Result/Downlaod_Content.csv", sep=',')
    else:
        df.to_csv("./Result/Downlaod_Content.csv", sep=',')
except FileNotFoundError:
    print("This is invalid account name. Try again.")
