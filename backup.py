#findind bluetooth connecting devices
import os
import plistlib
import time
import sqlite3
import csv
import re
import traceback
import getpass

def makecopy():
    script_folder=os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_folder)
    if os.path.isdir('./Copy_backup')==False:
        os.mkdir('./Copy_backup')
    now = script_folder+'/Copy_backup'
    
    #username=getpass.getuser()
    path = os.path.expanduser(f"~/Library/Application Support/MobileSync/")
    os.chdir(path)
    try:
        com = "cp -r Backup/ "+now
        os.popen(com)
        time.sleep(1)
        os.chdir(now)
    except:
        print("There is no Backup devices")

def CheckPlist():
    now = os.getcwd()

    rootdir = now
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            os.chdir(d+"/")
            now2=os.listdir()
            
            plist_name = "Info.plist"
            try:
                with open(plist_name, 'rb') as f:
                    plist_data = plistlib.load(f)
                    #print(plist_data)
                    #value_list = plist_data['\s']
                    script_folder=os.path.dirname(os.path.abspath(__file__))
    
                    now2 = script_folder
                    os.chdir(script_folder)
                    
                with open("TXT_backupinfo.txt", "w") as f:
                    #f.write("Mac address: ")
                    valuable_data=['GUID','IMEI','IMEI2','Last Backup Date','MEID','Product Name','Product Type','Product Version',
                                   'Serial Number','Target Identifier','Target Type','Unique Identifier']
                    for device_mac in plist_data.keys(): 
                        if device_mac in valuable_data:
                        #f.write(device_mac+"\n") #mac 주소
                            device_info = plist_data[device_mac]
                            #for i in device_info.keys():  
                            string = device_mac+" : "+str(device_info)
                            f.write(string+"\n")
                            f.write("\n")
                print(f"idevice backup output: {now2}")
                #print("Check The file, 'TXT_backupinfo.txt'")
            except:
                print("There is no backup devices in Mac")
                #print(traceback.format_exc())


def find_idevicebackup():
    try:
        makecopy()
        CheckPlist()
    except:
        return
    
