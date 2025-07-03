import os
import sys
import requests

usernameExists = False
usernameWarning = False
username = None

joinedServer = False
server = None

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
    global usernameExists, username, joinedServer, server

    if usernameExists == False:
        print("You don't have a username, to set one, type 'username'.")
        shell()

    while joinedServer == False:
        server = input("What is the domain name or IP of the server with the port? (ex. example.com or 192.168.123.132:8375) ")
        print("Joined server.")
        joinedServer = True

    game()

def game():
    pass

def shell():
    global usernameExists, username

    inShell = True

    versionFile = open("version.txt")
    version = versionFile.read()

    commandsFile = open("commands.txt")
    commands = commandsFile.read()

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
        else:
            print("error: didn't recognize that command")

clear()
print("Welcome to TerminalCasino!\nType 'help' to get a list of the commands.")
shell()
