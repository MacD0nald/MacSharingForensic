#findind bluetooth connecting devices
import os
import plistlib
import time
import sqlite3
import csv
import re
import traceback
def makecopy():
    if os.path.isdir('./copy_icloud')==False:
        os.mkdir('./copy_icloud')
    now = os.getcwd()+'/copy_icloud'
    
    username=input("Enter the username: ")
    path = "/Users/%s/Library/Preferences/"%username
    os.chdir(path)
    #print(now)
    com = "cp MobileMeAccounts.plist "+now+"/"+"accountinfo.plist"
    os.popen(com)
    time.sleep(3)
    os.chdir(now)

def CheckPlist():
    plist_name = "accountinfo.plist"
    try:
        with open(plist_name, 'rb') as f:
            plist_data = plistlib.load(f)
            #print(plist_data)
            value_list = plist_data["Accounts"]
        with open("accountinfo.txt", "w") as f:
            #f.write("Mac address: ")
            for device_mac in value_list[0].keys(): 
                f.write(device_mac+"\n") #mac 주소
                device_info = value_list[0][device_mac]
                #for i in device_info.keys():  
                string = device_mac+" : "+str(device_info)
                f.write(string+"\n")
                f.write("\n")
        print("Check The file, 'accountinfo.txt'")
    except:
        print("There is no devices in Mac")
        print(traceback.format_exc())


def TxttoCsv():
    
    header=[]
    valuableinfo=[]
    values=[]

    csv_file = 'output_icloud.csv'

    with open("accountinfo.txt",'r') as file:
        lines=file.readlines()
        valuableinfo.append(lines[1])
        valuableinfo.append(lines[4])
        valuableinfo.append(lines[7])
        valuableinfo.append(lines[10])
        valuableinfo.append(lines[13])
        valuableinfo.append(lines[16])
        valuableinfo.append(lines[19])
        for i in range(0,len(valuableinfo)):
            valuableinfo[i].split(":")
            header.append(valuableinfo[i].split(":")[0])
            values.append(valuableinfo[i].split(":")[1].replace(':',''))
    os.chdir('..')
    now2=os.getcwd()
    # Write the data to a CSV file
    with open(now2+'/'+csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the column names as the header row
        csv_writer.writerow(header)
        
        # Write the data rows
        csv_writer.writerow(values)

    print(f"Data has been exported to '{csv_file}'.")



    



def find_icloudaccount():
    makecopy()
    CheckPlist()
    TxttoCsv()

find_icloudaccount()
