import sys
import backup
import Calendar
import callhistory
import Contact
import download_check
import find_BTdevices
import icloudaccountinfo
import login_window
import NoteStore
import photos_value
import Spotlight_SearchResult
import Terminal_history
import webbrowser

def help():
    help_e = """

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣶⣶⣶⣦⠀⠀⠀⠀⠀⠀⣰⣶⣶⣶⡆⠀⠀⠀⣀⣤⣶⣶⣶⣶⣶⣶⣦⠀⠀⠀⢠⣶⣶⣶⣶⣶⣶⣶⣶⣶⡆⠀⠀
⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⠀⠀⠀⠀⢀⣼⣿⣿⣿⡿⠀⠀⢀⣾⣿⡿⠟⠋⠉⠙⠛⠿⠋⠀⠀⠀⣸⣿⡿⠛⠛⠛⠛⠛⠛⠛⠁⠀⠀
⠀⠀⠀⠀⠀⣸⣿⡿⢸⣿⣿⠀⠀⠀⣠⣿⡿⢻⣿⣿⠃⠀⠀⣾⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢰⣿⣿⠃⢸⣿⣿⠀⢀⣴⣿⠟⠀⣾⣿⠏⠀⠀⠈⣿⣿⣿⣷⣶⣦⣤⣀⠀⠀⠀⠀⢀⣿⣿⣯⣤⣤⣤⣤⣤⣤⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣿⣿⡏⠀⢸⣿⣿⣠⣾⡿⠃⠀⣸⣿⡟⠀⠀⠀⠀⠀⠙⠛⠻⠿⣿⣿⣿⣷⠀⠀⠀⣼⣿⣿⠿⠿⠿⠿⠿⠿⠇⠀⠀⠀⠀⠀
⠀⠀⠀⣼⣿⡿⠀⠀⢸⣿⣿⣿⠟⠀⠀⢰⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⡿⠀⠀⣰⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢰⣿⣿⠁⠀⠀⠀⠛⠛⠋⠀⠀⢀⣿⣿⡏⠀⠀⣠⣾⣶⣤⣀⣀⣀⣤⣾⣿⡿⠁⠀⢠⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠿⠿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠼⠿⠿⠀⠀⠀⠙⠿⠿⣿⣿⣿⣿⠿⠟⠉⠀⠀⠀⠾⠿⠿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

This tool is a Mac operating system forensics tool specific to Ventura(13.4.*)
It can collect some artifacts of Mac and show the result as CSV file.
if you want to see the explanation of the parameters, you can use "-h".

< Parameters >
 -all : all artifacts
 -bt : Bluetooth connecting devices
 -cale: Calendar
 -call: Call history
 -cont : command history
 -d: downlaods source
 -h : help
 -ic : icloud account
 -id : idevice backup
 -l : login history
 -n : Note
 -p : Photos
 -s : Spotlight
 -w : web browser[Chrome, Safari]
"""
    print(help_e)

value = sys.argv[1]
try:
    if len(sys.argv) <=1:
        help()
    if len(sys.argv) == 2:
        if value == '-bt':
            find_BTdevices.find_BTdevices()
        elif value =='-id':
            backup.find_idevicebackup()
        elif value == '-cale':
            Calendar.Calendar()
        elif value == '-call':
            callhistory.CallH()
        elif value == '-cont':
            Contact.Contact()
        elif value =='-d':
            download_check.Download_Check()
        elif value == '-ic':
            icloudaccountinfo.find_icloudaccount()
        elif value == '-l':
            login_window.login()
        elif value == '-n':
            NoteStore.Note()
        elif value =="-p":
            photos_value.Photos()
        elif value == "-s":
            Spotlight_SearchResult.Spotlight()
        elif value == "-t":
            Terminal_history.Terminal()
        elif value == "-w":
            webbrowser.webHistory()
        elif value == "-all":
            find_BTdevices.find_BTdevices()
            backup.find_idevicebackup()
            Calendar.Calendar()
            callhistory.CallH()
            Contact.Contact()
            download_check.Download_Check()
            icloudaccountinfo.find_icloudaccount()
            login_window.login()
            NoteStore.Note()
            photos_value.Photos()
            Spotlight_SearchResult.Spotlight()
            Terminal_history.Terminal()
            webbrowser.webHistory()
        else:
            help()
except Exception as e:
    error = f"""
    Try again. If you need a help, you can use "-h"
    error message : {e}

    """
    print(error)
