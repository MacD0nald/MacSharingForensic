#findind bluetooth connecting devices
import os
import plistlib
import time
import sqlite3
import csv
import re
def makecopy():
    script_folder=os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_folder)
    if os.path.isdir('./Copy_BT')==False:
        os.mkdir('./Copy_BT')
    now = script_folder+'/Copy_BT'  
    path = "/Library/Preferences/"
    os.chdir(path)
    #print(now)
    com = "cp com.apple.bluetooth.plist "+now+"/"+"bluetooth_log.plist"
    os.popen(com)
    time.sleep(3)
    os.chdir(now)

def CheckPlist():
    plist_name = "bluetooth_log.plist"
    script_folder=os.path.dirname(os.path.abspath(__file__))

    try:
        with open(plist_name, 'rb') as f:
            plist_data = plistlib.load(f)
            #print(plist_data)
            value_list = plist_data["PersistentPorts"]
        with open(script_folder+"/bluetooth_log.txt", "w") as f:
            #f.write("Mac address: ")
            for device_mac in value_list.keys(): 
                f.write(device_mac+"\n") #mac 주소
                device_info = value_list[device_mac]
                for i in device_info.keys():  
                    string = str(i)+" : "+str(device_info[i])
                    f.write(string+"\n")
                f.write("\n")
        print("Check The file, 'bluetooth_log.txt'")
    except:
        print("There is no devices in Mac")

def CheckDatabase():
    script_folder=os.path.dirname(os.path.abspath(__file__))

    now = script_folder+'/Copy_BT'  
    path = "/Library/Bluetooth/"
    os.chdir(path)
    #print(now)
    com = "cp com.apple.MobileBluetooth.ledevices.paired.db "+now+"/"+"bluetooth_log.db"
    os.popen(com)
    com1 = "cp com.apple.MobileBluetooth.ledevices.paired.db-shm "+now+"/"+"bluetooth_log.db-shm"
    os.popen(com1)
    com2 = "cp com.apple.MobileBluetooth.ledevices.paired.db-wal "+now+"/"+"bluetooth_log.db-wal"
    os.popen(com2)
    time.sleep(3)
    os.chdir(now)

def DbtoCsv():
    script_folder=os.path.dirname(os.path.abspath(__file__))

    os.chdir(script_folder)
    now = script_folder+'/Copy_BT'  
    database_file = now+"/"+"bluetooth_log.db"
    table_name = 'PairedDevices'
    csv_file = 'CSV_BT.csv'
    conn = sqlite3.connect(database_file)

    # Create a cursor object
    cursor = conn.cursor()

    # Execute a query to fetch data from the table
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)

    # Fetch all the rows from the query result
    data = cursor.fetchall()

    # Get the column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]+["type"]

    # Close the cursor and database connection
    cursor.close()
    conn.close()
    os.chdir(script_folder)
    # Write the data to a CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the column names as the header row
        csv_writer.writerow(column_names)
        
        # Write the data rows
        csv_writer.writerows(data)

    print(f"Data from '{table_name}' in '{database_file}' has been exported to '{csv_file}'.")

    with open("bluetooth_log.txt",'r') as file:
        lines=file.readlines()

    devices=[]    
    index=[]
   
    for line in lines:
        if line == '\n':
            index.append(lines.index(line))
    index_set = set(index)
    index=list(index_set)
    index.append(0)
    index.append(len(lines))
    index.sort()

    if len(index)==0:
        devices.append(lines)
    else:
        for i in range(0,len(index)-1):
              devices.append(lines[index[i]:index[i+1]])   
    mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    for j in range(0,len(devices)):
        global mac
        for k in range(0,len(devices[j])):
            devices[j][k]=devices[j][k].replace('\n','')
            if re.match(mac_pattern,devices[j][k]):
                mac=devices[j][k]
            elif 'BSDName' in devices[j][k]:
                name=devices[j][k]
            else: continue
        info=['',name,'',mac]
        with open(csv_file,'a',newline='') as f:
            csv_writer = csv.writer(f)
        
        # Write the column names as the header row
            csv_writer.writerow(info)
            
    #print(devices)



def find_BTdevices():
    makecopy()
    CheckPlist()
    CheckDatabase()
    DbtoCsv()

find_BTdevices()
