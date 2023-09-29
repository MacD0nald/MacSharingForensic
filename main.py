import sys
from backup import find_idevicebackup
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
 -bt : Bluetooth connecting devices
 -cale: Calendar
 -call: Call history
 -cont : command history
 -d: downlaods source
 -h : help
 -l : login history
 -p : installed programs' name
 -w : web browser[Chrome, Safari]
"""
    print(help_e)

value = sys.argv[0]
try:
    if len(sys.argv) <=1:
        help()
    if len(sys.argv) == 2:
        if value == '-bt':
            find_BTdevices
        elif value =='-id':
            find_idevicebackup()
        elif value == '-cale':
            Calendar
        elif value == '-call':
            callhistory
        elif value == '-cont':
            Contact
        elif value =='-d':
            download_check
        elif value == '-ic':
            icloudaccountinfo
        elif value == '-l':
            login_window
        elif value == '-n':
            NoteStore
        elif value =="-p":
            photos_value
        elif value == "-s":
            Spotlight_SearchResult
        elif value == "-t":
            Terminal_history
        elif value == "w":
            webbrowser
        else:
            help()
except Exception as e:
    error = f"""
    Try again. If you need a help, you can use "-h"
    {e}

    """
    print(error)