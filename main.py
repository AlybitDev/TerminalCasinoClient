import os
import requests
import sys
import json

usernameExists = False
usernameWarning = False
username = None

joinedServer = False
serverURL = None

version = None
versionJSON = None

uuid = None

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
                print("This already was your password.")
                usernameWarning = False
                usernameExists = True
            else:
                print("Username reset.")
                username = usernameRequest
                usernameWarning = False
                usernameExists = True

    shell()

def joinServer():
    global uuid, usernameExists, username, joinedServer, serverURL, versionJSON

    if usernameExists == False:
        print("You don't have a username, to set one, type 'username'.")
        shell()

    while joinedServer == False:
        print("What is the domain name or IP of the server with the port? (ex. http://example.com/ or http://192.168.123.132:8375/)")
        serverURL = input("> ")
        versionInJSON = versionJSON['version']
        joinObj = {'name': username, 'version': versionInJSON}
        joinServerPOST = requests.post(serverURL + "join", json = joinObj).json()
        if 'error' in joinServerPOST:
            print(joinServerPOST['error'])
            serverURL = None
        else:
            print(joinServerPOST['response'])
            uuid = joinServerPOST['uuid']
            joinedServer = True

    shell()

def joinRoom():
    global serverURL

def createRoom():
    global uuid, serverURL

    print("What game do you want to play in the room?\nGames: Roulette(1)")
    gameToPlay = input("> ")
    createRoomObj = {'uuid': uuid, 'game': gameToPlay}
    createRoomPOST = requests.post(serverURL + "createroom", json=createRoomObj).json()


def shell():
    global usernameExists, username, version, versionJSON

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
            if usernameExists == True:
                print("You already have a username set, it is " + username + ". To reset your username, type 'username reset'.")
            else:
                usernameShell()
        elif command == "username reset":
            if usernameExists == False:
                print("You don't have a username set. To set one, type 'username'.")
            else:
                usernameExists = False
                usernameShell()
        elif command == "echo username":
            if username == None:
                print("You need to set your username before using this command. To set your username, type 'username'.")
            else:
                print(username)
        elif command == "server":
            joinServer()
        elif command == "clear":
            clear()
        elif command == "room":
            if joinedServer == False:
                print("You need to join a server before you can create or join a room.")
            else:
                print("Do you wanna join a room or create one? (1) Create (2) Join")
                roomQuestion = input("> ")
                if roomQuestion == "2":
                    print("What is the room code?")
                    roomCode = input("> ")
                    joinRoom()
                elif roomQuestion == "1":
                    pass
        else:
            print("error: didn't recognize that command")

clear()
print("Welcome to TerminalCasino!\nType 'help' to get a list of the commands.")
shell()
