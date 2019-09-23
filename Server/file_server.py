import sys
import socket
import codecs
import time
from lib import Lib

HOST = '10.0.0.1'
PORT = 9000
BUFSIZE = 1000

def main(argv):
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.bind(('', PORT))
	serverSocket.listen(1)
	print('The server is running and ready to receive')

	while True:
		connectionSocket, addr = serverSocket.accept()
		printConnectionEstablished(connectionSocket)
		print('Waiting to recieve file name')
		fileName = ''
		fileSize = ''
		fileName = getTargetFile(connectionSocket)
		fileSize = getTargetFileSize(fileName)
		Lib.writeTextTCP(str(fileSize), connectionSocket)
		sendFile(fileName, fileSize, connectionSocket)
		time.sleep(1)
		connectionSocket.close()


def sendFile(fileName,  fileSize,  conn):
	remainingFileSize = int(fileSize)
	fileToTransfer = open(fileName,"rb")
	while True:
		if remainingFileSize > 0:
			data = fileToTransfer.read(BUFSIZE)
			writeBinaryTCP(data, conn)
			remainingFileSize -= len(data)
			print('Bytes sent: ', len(data))
			print('Remaining file size: ', remainingFileSize)
		elif remainingFileSize <= 0:
			break

	print('All data has been sent')
	fileToTransfer.close()

def writeBinaryTCP(binary, conn):
	conn.send(binary)

def readBinaryTCP(conn):
	msg = ""
	msg = conn.recv(1)

	return msg

def getTargetFile(conn):
	targetFileName = ""
	targetFileName = Lib.readTextTCP(conn)
	print('Extracting:')
	print(targetFileName)
	return targetFileName

def getTargetFileSize(targetFileName):
	targetFileSize = ""
	targetFileSize = Lib.check_File_Exists(Lib.extractFilename(targetFileName))
	print('Size:')
	print(targetFileSize)
	return targetFileSize


def printConnectionEstablished(conn):
	receivedMessage = Lib.readTextTCP(conn)
	print(receivedMessage)
	Lib.writeTextTCP('Server is ready to recieve file name', conn)

if __name__ == "__main__":
		main(sys.argv[1:])
