# nota-RAT - Simple reverse shell with python using encryption

## What is nota-RAT?
nota-RAT is basically a reverse shell using sockets in python for windows 10+.

1. The RAT binds sockets together so that the attacker can connect.
2. Then it will ask wether you want to enable OTP, if so then you put in the required info then you get a qrcode to scan in your OTP app
3. after you connect as the attacker you can run pretty much any cli command
4. When a command is send it uses Fernet for end to end encryption

## Features
* Encryption
* * nota-RAT uses the python library Fernet for encryption
* * Fernet uses AES in CBC mode with a 128-bit key for encryption; using PKCS7 padding
* Discord webhooks
* * nota-RAT uses the pythom library discord_webhook for discord web hooks
* * The web hooks display the IP of the victim and shows the avg ping of the connection
* Get/Send files
* * nota-RAT can get and send files from the files direcotry into the RAT's CWD
* * This can we used to send additional malware to the victim's PC
* Live feed
* * nota-RAT uses the vidstream library to get a live feed of the victim's screen
* OTP
* * nota-RAT can be used with OTP to have a level of authentication

## How to install and run?
   
Cloning using git.

1. Clone the repo
   ```sh
   git clone https://github.com/fluffydolphin/not-RAT.git
   pip install -r requirements.txt
   ```
   
2. cd into not-RAT
   ```sh
   cd nota-RAT
   ```
   
2. cd into server or RAT
   ```sh
   cd attacker
   ```
   ```sh
   cd RAT
   ```
   
3. Run command for either server or RAT
   ```sh
   sudo python attacker.py
   ```
   ```sh
   python RAT.py
   ```
  
That's all it takes to install and run nota-RAT.

## Commands and Configuration for nota-RAT.
It is possible to modify the behaviour of nota-RAT with cli
arguments. In order to get an up-to-date help document, just run
`attacker -h`.

you can change the server ip on the client and bot but not on the server, the default host ip on the server is 0.0.0.0 (localhost)

* -p, --port
* * Port of the Server, default 423
* -d, --discord
* * After you have added discord webhooks as a argument then you need to specify your webhooks URL
* * Example: python attacker.py -p 5000 -d https://discord.com/api/webhooks/your-webhook-url

---------------------------------------------------------------------------------------------------------------------------------------------------------

These commands are for after you have started nota-RAT and adjusted the behaviour

* /help                      
* * Print this message.
* /getlive                   
* * Gets a live feed of victim's screen.
* /stoplive                  
* * Stop the live feed of victim's screen.
* /sendfile                  
* * Sends a file from the files directory in the victom's CWD directory.
* /getfile                   
* * Gets a file from the victim's CWD and puts it into the files directory.
* /config
* * Allows you to change the config file
* /clear                     
* * Clear screen.
* /exit/quit/q               
* * Close session and exit.
