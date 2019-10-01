import sys
import socket
from lib import Lib

SERVERNAME = '10.0.0.1'
SERVERPORT = 27777
BUFSIZE = 1000

def main(argv):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        userInput = ''
        userInput = waitForUserInput()
        clientSocket.sendto(userInput,(SERVERNAME, SERVERPORT))
        filePath, addr = clientSocket.recvfrom(BUFSIZE)
        print(filePath)


def waitForUserInput():
    inputAccepted = False
    while not inputAccepted:
        print('Input command')
        userInput = raw_input()
        if userInput == 'u' or userInput == 'U' or userInput == 'l' or userInput == 'L':
            inputAccepted = True
        else:
            inputAccepted = False
            print('Accepted values are: u for uptime and l for load')
    return userInput

if __name__ == "__main__":
    main(sys.argv[1:])
