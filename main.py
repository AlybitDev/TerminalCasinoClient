import os
import requests
import sys
import json
import threading
from websockets.sync.client import connect

usernameExists = False
usernameWarning = False
username = None

inServer = False
serverURL = None

version = None
versionJSON = None

uuid = None

roomCode = None
inRoom = False

def clear():
    os.system('cls||clear')

def usernameShell():
    global usernameExists, usernameWarning, username

    while usernameExists == False:
        print("What do you want to be your username?\nYou're username must be between 3 and 32 characters.")
        if usernameWarning == True:
            print("Your username is too long or too short.")
        usernameRequest = input("> ")
        if len(usernameRequest) < 3 or len(usernameRequest) > 32:
            usernameWarning = True
        else:
            if username == None:
                print("Username set.")
                username = usernameRequest
                usernameWarning = False
                usernameExists = True
            elif username == usernameRequest:
                print("This already was your username.")
                usernameWarning = False
                usernameExists = True
            else:
                print("Username reset.")
                username = usernameRequest
                usernameWarning = False
                usernameExists = True

def joinServer():
    global uuid, usernameExists, username, inServer, serverURL, versionJSON

    while inServer == False:
        realServer = False

        while realServer == False:
            print("What is the domain name or IP of the server with the port? (ex. example.com/ or 192.168.123.132:8375/)")
            serverURL = input("> ")
            versionInJSON = versionJSON['version']
            joinObj = {'name': username, 'version': versionInJSON}

            try:
                joinServerPOST = requests.post("http://" + serverURL + "join", json=joinObj).json()
            except requests.exceptions.RequestException:
                print("Connection failed. Please give a valid domain name or IP.")
                continue
            except json.JSONDecodeError:
                print("This server exists, but isn't running TerminalCasinoServer. Please give a valid domain name or IP.")
                continue

            realServer = True

        if 'error' in joinServerPOST:
            print(joinServerPOST['error'])
            serverURL = None
        else:
            print(joinServerPOST['response'])
            uuid = joinServerPOST['uuid']
            inServer = True

def joinRoom(room):
    global uuid, serverURL, roomCode, inRoom

    joinRoomObj = {'uuid': uuid, 'room': room}
    joinRoomPOST = requests.post("http://" + serverURL + "joinroom", json=joinRoomObj).json()

    if "error" in joinRoomPOST:
        print(joinRoomPOST["error"])
    else:
        print(joinRoomPOST["response"])
        roomCode = room
        inRoom = True

def createRoom():
    global uuid, serverURL, inRoom, roomCode

    gameChosen = False

    while gameChosen == False:

        print("What game do you want to play in the room?\nGames: Roulette(1)")
        gameToPlay = input("> ")
        if gameToPlay == "1":
            gameChosen = True
        else:
            print("You need to type a number.")

    moneyChosen = False

    while moneyChosen == False:
        print("What do you want the starting money to be? (Only numbers)")
        money = input("> ")
        if money.isdigit():
            moneyChosen = True
        else:
            print("You need to type a numeral.")

    createRoomObj = {'uuid': uuid, 'game': int(gameToPlay), 'money': int(money)}
    createRoomPOST = requests.post("http://" + serverURL + "createroom", json=createRoomObj).json()

    roomCode = createRoomPOST["roomcode"]
    print(createRoomPOST["response"] + " The room code is " + roomCode + ".")
    inRoom = True

def roomPlayers():
    global uuid, serverURL

    roomPlayersObj = {'uuid': uuid}
    roomPlayersPOST = requests.post("http://" + serverURL + "roomplayers" , json=roomPlayersObj).json()

    if 'error' in roomPlayersPOST:
        print(roomPlayersPOST['error'])
    else:
        totalPlayers = int(roomPlayersPOST['players'])
        print("Players in this room(" + str(totalPlayers) + "):")

        for key in range(1, totalPlayers + 1):
            key = str(key)
            print(roomPlayersPOST[key])

def leaveRoom():
    global uuid, inRoom, roomCode

    leaveRoomObj = {'uuid': uuid}
    leaveRoomPOST = requests.post("http://" + serverURL + "leaveroom", json=leaveRoomObj).json()

    if 'error' in leaveRoomPOST:
        print(leaveRoomPOST['error'])
    else:
        print(leaveRoomPOST['response'])
        inRoom = False
        roomCode = None

def startGame():
    global uuid, serverURL

    with connect("ws://" + serverURL + "game") as ws:
        while True:
            ws.send(uuid)
            data = ws.recv()
            print(data)

def shell():
    global usernameExists, username, version, versionJSON, serverURL, inRoom, roomCode

    inShell = True

    versionFile = open("version.txt")
    version = versionFile.read()
    versionFile.close()

    commandsFile = open("commands.txt")
    commands = commandsFile.read()
    commandsFile.close()

    with open('version.json', 'r') as versionJSONFile:
        versionJSON = json.load(versionJSONFile)

    while inShell == True:
        command = input(">>> ")
        if command == "exit":
            sys.exit("Exited")
        elif command == "version":
            print(version)
        elif command == "help":
            print(commands)
        elif command == "username":
            if inServer:
                print("You are in a server so you can't chance your username.")
            elif usernameExists == True:
                print("You already have a username set, it is " + username + ". To reset your username, type 'username reset'.")
            else:
                usernameShell()
        elif command == "username reset":
            if usernameExists == False:
                print("You don't have a username set. To set one, type 'username'.")
            elif inServer:
                print("You are in a server so you can't chance your username.")
            else:
                usernameExists = False
                usernameShell()
        elif command == "echo username":
            if username == None:
                print("You need to set your username before using this command. To set your username, type 'username'.")
            else:
                print(username)
        elif command == "server":
            if usernameExists == False:
                print("You don't have a username, to set one, type 'username'.")
            elif inServer == False:
                joinServer()
            else:
                print("You already joined a server, it's URL is " + serverURL + ".")
        elif command == "echo server":
            if inServer == False:
                print("You need to be in a server to use this command.")
            else:
                print(serverURL)
        elif command == "clear":
            clear()
        elif command == "room join":
            if inServer == False:
                print("You need to join a server before you can join a room.")
            elif inRoom:
                print("You already are in a room.")
            else:
                print("What is the room code?")
                room = input("> ")
                joinRoom(room)
        elif command == "room create":
            if inServer == False:
                print("You need to join a server before you can create a room.")
            elif inRoom:
                print("You already are in a room.")
            else:
                createRoom()
        elif command == "room code":
            if inRoom:
                print(roomCode)
            else:
                print("You need to be in a room to use this command.")
        elif command == "room players":
            if inRoom:
                roomPlayers()
            else:
                print("You need to be in a room to use this command.")
        elif command == "room leave":
            if inRoom:
                leaveRoom()
            else:
                print("You need to be in a room to use this command.")
        else:
            print("error: didn't recognize that command")

clear()
print("Welcome to TerminalCasino!\nType 'help' to get a list of the commands.")
shell()
