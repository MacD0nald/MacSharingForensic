#Check Safari history
import sqlite3
import os
import time
import plistlib
import datetime
import pandas as pd


def makecopy(history, now, web):
    Copy_folder = now+"/Copy_"+web+"history/"
    if not(os.path.isdir(Copy_folder)):
        os.mkdir(Copy_folder)
    if web == "Safari":
        os.chdir(history)
        com = "cp History.db "+Copy_folder+"Safari_history.db"
        os.popen(com)
        time.sleep(1)
        com = "cp Downloads.plist "+Copy_folder+"Safari_download.plist"
        os.popen(com)
        time.sleep(1)
    elif web == "Chrome":
        os.chdir(history)
        com = "cp History "+Copy_folder+"/chrome_history"
        os.popen(com)
        time.sleep(1)
    

def checkDownload(web, now_path): #Check the Safari Download history
    Copy_folder = now_path+"/Copy_"+web+"history/"
    download = []
    if web == "Safari":
        with open(os.path.join(Copy_folder, 'Safari_download.plist'), 'rb') as f:
            plist_data = plistlib.load(f)
        #plist_name = "./Copy_Safarihistory/Safari_download.plist"
        #checklist = ['DownloadEntryProgressTotalToLoad', 'DownloadEntryDateAddedKey', 'DownloadEntryDateFinishedKey', 'DownloadEntryURL', 'DownloadEntryPath']
        #DownloadEntryProgressTotalToLoad = File's byte size 
        #DownloadEntryDateAddedKey = Download start time (datetime)/DownloadEntryDateFinishedKey = Download finish time
        #DownloadEntryURL = Download url
        #DownloadEntryPath = Path to downloaded file
            for i in plist_data["DownloadHistory"]:
                size = ''
                start_time = ''
                finish_time = ''
                url = ''
                path = ''
                for j in i.keys():
                    if j == "DownloadEntryProgressTotalToLoad":
                        size = i[j]
                    elif j == "DownloadEntryDateAddedKey":
                        start_time = i[j]
                    elif j == "DownloadEntryDateFinishedKey":
                        finish_time = i[j]
                    elif j == "DownloadEntryURL":
                        url = i[j]
                    elif j == "DownloadEntryPath":
                        path = i[j]
                download.append([start_time, finish_time, path, size, url])
            col = ["start_time", "finish_time", "DownloadPath", "ByteSize","DownloadURL"]
            df = pd.DataFrame(download, columns=col)
            os.chdir(now_path)
            # CSV 파일로 저장
            csv_file = os.path.join(now_path, 'CSV_SafariDownload.csv')  # CSV 파일 경로 설정
            df.to_csv(csv_file, sep=',')
            print("Safari Download output : ", csv_file)

    if web == "Chrome":
        download = []
        con = sqlite3.connect(os.path.join(Copy_folder, 'chrome_history'))
        cursor = con.cursor()
        cursor.execute("SELECT start_time, target_path, tab_url FROM downloads")
        data = cursor.fetchall()
        con.close()
        for i in data:
            date = i[0]/1000000 - 11644473600
            date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
            download.append([date, i[1], i[2]])
        col = ["Start time", "Path", "url"]
        df = pd.DataFrame(download, columns=col)
    
        os.chdir(now_path)
        # CSV 파일로 저장
        csv_file = os.path.join(now_path, 'CSV_ChromeDownload.csv')  # CSV 파일 경로 설정
        df.to_csv(csv_file, sep=',')
        print("Chrome Download output : ", csv_file)


def checkUrl(web, now_path):  #check the visited url
    Copy_folder = now_path+"/Copy_"+web+"history/"
    if web == "Safari":
        db_name = os.path.join(Copy_folder, "Safari_history.db")
        #print(db_name)
        con = sqlite3.connect(db_name)
        cursor = con.cursor()
        cursor.execute("SELECT visit_time, title FROM history_visits")
        col = ["visit title", "title"]
        data = cursor.fetchall()
        con.close()
        visit = []
        for i in data:
            base_date = datetime.datetime(2001, 1, 1)
            dt_object = base_date + datetime.timedelta(seconds=i[0])
            date = dt_object.strftime('%Y-%m-%d %H:%M:%S') + " (UTC+0)"
            visit.append([date, i[1]])
        df = pd.DataFrame(visit, columns=col)
        os.chdir(now_path)
        # CSV 파일로 저장
        csv_file = os.path.join(now_path, 'CSV_SafariVisit.csv')  # CSV 파일 경로 설정
        df.to_csv(csv_file, sep=',')
        print("Safari Visit output : ", csv_file)
    elif web == "Chrome":
        visit = []
        con = sqlite3.connect(os.path.join(Copy_folder, 'chrome_history'))
        cursor = con.cursor()
        cursor.execute("SELECT last_visit_time, url, title, visit_count FROM urls")
        data = cursor.fetchall()
        con.close()
        for i in data:
            date = i[0]/1000000 - 11644473600
            date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
            visit.append([date,i[2], i[1], i[3]])
        col = ['Last visit time', 'Title', 'Url', 'Visit count']

        df = pd.DataFrame(visit, columns=col)
        os.chdir(now_path)
        # CSV 파일로 저장
        csv_file = os.path.join(now_path, 'CSV_ChromeVisit.csv')  # CSV 파일 경로 설정
        df.to_csv(csv_file, sep=',')
        print("Chrome Visit output : ", csv_file)

def checkWeb():
    lib_path =os.path.expanduser(f"~/Library/")
    # 현재 스크립트 파일이 있는 폴더 경로
    now_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(lib_path)
    stream = os.popen("ls")
    folder_name = stream.readlines()
    safari = False
    google = False

    for i in folder_name: 
        if "Safari\n" in i:
            #print("Safari matched!") 
            history = lib_path+"/Safari"
            makecopy(history, now_path, "Safari")
            os.chdir(now_path)
            checkUrl("Safari", now_path)
            checkDownload("Safari", now_path)
            safari = True
        elif "Google" in i:
            #print("Google matched!")
            history_path = lib_path + "/Application Support/Google/Chrome/Default"
            makecopy(history_path, now_path, "Chrome")
            os.chdir(now_path)
            checkDownload("Chrome", now_path)
            checkUrl("Chrome", now_path)
            google = True
    if not(safari or google):
        print("There is no Safari and Chrome")

def webHistory():
    checkWeb()
