import os
import sqlite3
import csv
import datetime
import time
import getpass

def makecopy():
    if os.path.isdir('./Copy_Calendar')==False:
        os.mkdir('./Copy_Calendar')
    now = os.getcwd()+'/Copy_Calendar'

    username = getpass.getuser()

    path = "/Users/"+username+"/Library/Calendars"
    os.chdir(path)
    #print(now)
    com = "cp Calendar.sqlitedb "+ now +"/"+"Calendar.sqlitedb"
    os.popen(com)
    time.sleep(3)
    os.chdir(now)

def convert_coretime_to_readable(timestamp):
     # Mac Absolute Time (CoreServices Timestamp)는 2001년 1월 1일 기준
    base_date = datetime.datetime(2001, 1, 1)

    # timedelta 객체를 사용해 초를 추가
    dt_object = base_date + datetime.timedelta(seconds=timestamp)

    # 원하는 포맷으로 datetime 객체를 문자열로 변환
    readable_time = dt_object.strftime('%Y-%m-%d %H:%M:%S') + " (UTC+0)"

    return readable_time


def sqlite_to_csv(database, file_name):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT CalendarItem.ROWID, summary, description, start_date, end_date, creation_date, CalendarItem.last_modified, CalendarItem.url, AttachmentFile.filename, AttachmentFile.url, local_path, download_tries, Location.title, address, latitude, longitude, Participant.email, phone_number, comment\nFROM CalendarItem\nLEFT OUTER JOIN Attachment ON CalendarItem.ROWID = Attachment.owner_id\nLEFT OUTER JOIN AttachmentFile ON Attachment.file_id = AttachmentFile.ROWID\nLEFT OUTER JOIN Location On CalendarItem.ROWID = Location.item_owner_id\nLEFT OUTER JOIN Participant On CalendarItem.ROWID = Participant.owner_id;")
    rows = cursor.fetchall()

    column_names = ['Row_id', 'title', 'description', 'start_date', 'end_date', 'created_time', 'last_modified_time', 'added_url', 'file_name', 'file_url', 'file_local_path', 'file_download_tries', 'location_name', 'location_address', 'latitude', 'longtitude', 'participant_email', 'participant_phone', 'participant_comment']

    converted_rows = []
    for row in rows:
        if row[3] is None:
            converted_start_date = "Empty"
        else:
          converted_start_date = convert_coretime_to_readable(row[3])

        if row[4] is None:
          converted_end_date = "Empty"
        else:
          converted_end_date = convert_coretime_to_readable(row[4])

        if row[5] is None:
          converted_created_date = "Empty"
        else:
          converted_created_date = convert_coretime_to_readable(row[5])

        if row[6] is None or row[6] < 0:
          converted_last_modified_date = "Empty"
        else:
          converted_last_modified_date = convert_coretime_to_readable(row[6])


        converted_row = (row[0], row[1], row[2], converted_start_date, converted_end_date, converted_created_date, converted_last_modified_date, row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18])
        converted_rows.append(converted_row)

    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_names)
        csv_writer.writerows(converted_rows)

    conn.close()

now = os.getcwd()

makecopy()

input_data = now+"/Copy_Calendar/Calendar.sqlitedb"
file_name = now+"/"+"Calendar.csv"
sqlite_to_csv(input_data, file_name)