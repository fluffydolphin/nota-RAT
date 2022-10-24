import socket
import argparse
import sys

parser = argparse.ArgumentParser(
    description="HiveMind, python bot net using sockets."
)

parser.add_argument("host", nargs="?", help="Address of the Server.")

parser.add_argument(
    "-p", "--port", default=420, help="Port the Server is running on.", type=int
)

parser.add_argument(
    "-b",
    "--bot",
    dest="bot",
    default="vers",
    type=str,
    help="The bot number this is.",
)

args = parser.parse_args()


if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

if not args.host:
    print("Host required! \n")
    parser.print_help()
    sys.exit(1)


HEADER = 64
PORT = args.port
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = args.host
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

while True:
    send(input())


send(DISCONNECT_MESSAGE)