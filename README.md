# nota-RAT - Simple reverse shell with python using encryption

## What is nota-RAT?
nota-RAT is basically a reverse shell using sockets (for connections) in python that can run pretty much all cli commands in Linux, Windows and MacOS (but has only been properly tested in Ubuntu Linux and Windows 10, 11).

1. The RAT binds sockets together so that the attacker can connect.
2. after you connect as the attacker you can run pretty much any cli command
3. When a command is send it uses Fernet for end to end encryption

## Features
* Encryption
* * nota-RAT uses the python library Fernet for encryption
* * Fernet uses AES in CBC mode with a 128-bit key for encryption; using PKCS7 padding
* Discord webhooks
* * nota-RAT uses the pythom library discord_webhook for discord web hooks
* * The web hooks display the IP of the victim and shows the avg ping of the connection

## How to install and run?

How to install git for cloning

1. Install git
   ```sh
   sudo apt install git
   ```
   
Cloning using git.

1. Clone the repo
   ```sh
   git clone https://github.com/fluffydolphin/not-RAT.git
   ```
   
2. Cd into not-RAT
   ```sh
   cd nota-RAT
   ```
   
2. Cd into server or RAT
   ```sh
   cd server
   ```
   ```sh
   cd RAT
   ```
   
3. Run command for either server or RAT
   ```sh
   sudo python3 server (you have to run as sudo or as admin or else the /getfile and /sendfile commands will not work)
   ```
   ```sh
   python3 RAT
   ```
  
That's all it takes to install and run nota-RAT.

## Commands and Configuration for nota-RAT.
It is possible to modify the behaviour of nota-RAT with cli
arguments. In order to get an up-to-date help document, just run
`attacker -h`.

you can change the server ip on the client and bot but not on the server, the default host ip on the server is 0.0.0.0 (localhost).

* -p, --port
* * Port of the Server, default 423


These commands are for after you have started nota-RAT and adjusted the behaviour

* exit
* * quits the script
* /sendfile
* * can send a file from the DIR that the script was run from
* /getfile
* * can get a file from the current DIR of the reverse shell
