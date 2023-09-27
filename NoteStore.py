import os
import sqlite3
import csv
import datetime
import time
import zlib
import getpass

def makecopy():    
    if os.path.isdir('./Copy_NoteStore')==False:
        os.mkdir('./Copy_NoteStore')
    now = os.getcwd()+'/Copy_NoteStore'
    #'/Users/mansoo/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite'
    
    username = getpass.getuser()
    
    path = "/Users/"+username+"/Library/Group Containers/group.com.apple.notes/"
    os.chdir(path)
    
    com = "cp NoteStore.sqlite "+now+"/"+"NoteStore.sqlite"
    os.popen(com)
    time.sleep(3)
    os.chdir(now)

def convert_coretime_to_readable(timestamp):
    base_date = datetime.datetime(2001, 1, 1)

    dt_object = base_date + datetime.timedelta(seconds=timestamp)
    
    readable_time = dt_object.strftime('%Y-%m-%d %H:%M:%S') + " (UTC+0)"

    return readable_time

def convert_hex_to_korean(blob_data):
    hex_data = ''.join([f"{byte:02x}" for byte in blob_data])
    byte_data = bytes.fromhex(hex_data)

    decompressed_data = zlib.decompress(byte_data, 16+zlib.MAX_WBITS)

    pattern_behind = b'\x1a\x10\n\x04\x08'
    idx = decompressed_data.find(pattern_behind)

    if idx != -1:
        decompressed_data = decompressed_data[:idx]

    korean_data = []
    i = 0
    while i < len(decompressed_data):
        found = False
        for size in range(4, 0, -1):
            try:
                chunk = decompressed_data[i:i+size]
                decoded = chunk.decode('utf-8')
                if decoded:
                    korean_data.append(decoded)
                    i += size
                    found = True
                    break
            except UnicodeDecodeError:
                continue

        if not found:
            i +=1

    return ''.join(korean_data)

def sqlite_to_csv(database, file_name):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT ZICCLOUDSYNCINGOBJECT.ZCREATIONDATE3, ZMODIFICATIONDATE1, ZSNIPPET, ZTITLE1, ZFILENAME, ZICNOTEDATA.ZDATA\nFROM ZICCLOUDSYNCINGOBJECT, ZICNOTEDATA\nWHERE ZICCLOUDSYNCINGOBJECT.Z_PK = ZICNOTEDATA.ZNOTE;")
    rows = cursor.fetchall()

    column_names = ['created_time', 'last_modified_time', 'snippet', 'title', 'note_data']

    converted_rows = []

    for row in rows:
        if row[0] is None:
            converted_creation_date = "Empty"
        else:
          converted_creation_date = convert_coretime_to_readable(row[0])
        
        if row[1] is None:
          converted_modified_date = "Empty"
        else:
          converted_modified_date = convert_coretime_to_readable(row[1])
        
        if row[4] is None:
            readable_hex_data = "Empty"
        else:
            readable_hex_data = convert_hex_to_korean(row[4])
        converted_row = (converted_creation_date, converted_modified_date, row[2], row[3], readable_hex_data)
        converted_rows.append(converted_row)

    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_names)
        csv_writer.writerows(converted_rows)

    conn.close()

now = os.getcwd()

makecopy()

hex_data = now+"/Copy_NoteStore/NoteStore.sqlite"
file_name = now+"/"+"NoteStore.csv"
sqlite_to_csv(hex_data, file_name)
