import sys
from socket import *
from lib import Lib

SERVERPORT = 9000
BUFSIZE = 1000
#SMALL = 'test.webp'
#BIG = 'lenna.png'
#DICKBUTT = 'Image.jpg'
ip =''
file=''

def main(ip, file):
	print('ip: ', ip)
	print('file: ', file)
	clientSocket = socket(AF_INET, SOCK_STREAM)
    	clientSocket.connect((ip, SERVERPORT))
    	Lib.writeTextTCP('Client initiated TCP connection', clientSocket)
	printServerResponse(clientSocket)
	sizeOfFile = int(requestFile(file, clientSocket))
	receiveFile(file, clientSocket, sizeOfFile)
    	clientSocket.close()


def receiveFile(file,  conn, fileSize):
	print('Writing data to file: ', file)
	dataRemaining = fileSize
	dataLength = 0
	print(dataRemaining)
	file = open(file, 'wb')

	while True:
		if dataRemaining >= BUFSIZE:
			data = readBinaryTCP(conn, BUFSIZE)
		elif dataRemaining <  BUFSIZE and dataRemaining > 0:
			print('Data is less than 1000 bytes, it is: ', dataRemaining)
			data = readBinaryTCP(conn, dataRemaining)
		else:
			break

		print('Writing to file ..')
		file.write(data)
		dataRemaining -= len(data)
		print('Data remaining: ', dataRemaining)

	file.close()
	print('File transer complete')

def writeBinaryTCP(file, conn):
	conn.send(file)

def readBinaryTCP(conn, dataLength):
	msg = ""
	dataRead = 0
	countDown = dataLength
	print('Count down is set to: ', countDown)

	while countDown > 0:
		ch = conn.recv(1)
		msg += ch
		countDown -= 1
		dataRead += 1

	print('Data read: ', dataRead)
	return msg

def requestFile(file, conn):
	print('Requesting file')
	Lib.writeTextTCP(file, conn)
	fileSize = Lib.getFileSizeTCP(conn)
	print('Size is: ', fileSize)
	print('Requesting,', file)
	Lib.writeTextTCP('Ready to receive', conn)
	return fileSize

def printServerResponse(conn):
    serverResponse = Lib.readTextTCP(conn)
    print('From Server:', serverResponse.decode())

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])
	ip = sys.argv[1]
	file = sys.argv[2]
