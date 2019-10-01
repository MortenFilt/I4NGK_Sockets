import sys
import socket
import codecs
import time
from lib import Lib

HOST = '10.0.0.1'
PORT = 27777
BUFSIZE = 1000
UPTIME = '/proc/uptime'
LOAD = '/proc/loadavg'

def main(argv):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('', PORT))
    print('UDP server is running')

    while True:
        clientMessage, addr = serverSocket.recvfrom(BUFSIZE)
        sendFile(clientMessage, addr, serverSocket)



def clientMessageHandler(choice):
    return {
        'u': UPTIME,
        'U': UPTIME,
        'l': LOAD,
        'L': LOAD,
        }[choice]

def sendFile(reqFile, addr, server):
    fileToTransfer = open(clientMessageHandler(reqFile),"rb")
    data = fileToTransfer.read(BUFSIZE)
    while True:
        server.sendto(data, addr)
        data = fileToTransfer.read(BUFSIZE)
        if not data:
            break

if __name__ == "__main__":
		main(sys.argv[1:])
