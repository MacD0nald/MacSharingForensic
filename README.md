# Mac Sharing Forensic

## Purpose

As MacOS versions continue to emerge, this tool allows users to collect differentiated artifacts generated by interworking between iDevices and iDevices related to file sharing that are different in paths from existing versions and other OSs, and show them in an easy-to-see form of output. Mac Sharing Forensic can be run against a live system

This tool was submitted to DFC Tech Contest.

## Requirements

- Python 3.9 or earlier
- MacOS Ventrura(13.4.*), for live collection

```bash
pip install -r requirements.txt
```

## Main Functions

- General Artifact
    - Login Window
    - Spotlight
    - Terminal History(zsh, bash)
- Mac Sharing Artifact
    - Bluetooth
    - Calendar
    - Call History
    - Contact
    - Download Files (Airdrop, SNS, WebBrowser, etc)
    - iCloud
    - iDevice Backup
    - Notes(메모)
    - Photos

## Usage

At its simplest, you can run ‘Mac Sharing Forensic’ with the following invocation.

```bash
sudo python3 main.py -all
```

If you want to know more about the tool parameters, type ‘-h’

```bash
python3 main.py -h
```

If you want to spin each of the artifacts, see below

```bash
python3 main.py [argv]
```

```bash
 -all : all artifacts
 -bt : Bluetooth connecting devices
 -cale: Calendar
 -call: Call history
 -cont : Contact
 -d: downlaods source
 -h : help
 -ic : icloud account
 -id : idevice backup
 -l : login history
 -n : Note
 -p : Photos
 -s : Spotlight
 -w : web browser[Chrome, Safari]
```
