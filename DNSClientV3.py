# Author: Guobao Sun
# Fall 2016 CSci4211: Introduction to Computer Networks
# This program serves as the client of DNS query.
# Written in Python v3.

import sys
from socket import *
from datetime import datetime

def main():
	logFile = open('client_log.txt', "a")	
	logFile.write(str(datetime.now()) + ": Client starts.\n")
	logFile.close()
	while 1:
		host = "localhost" # Remote hostname. It can be changed to anything you desire.
		port = 5001 # Port number.

		try:
			cSock = socket(AF_INET, SOCK_STREAM)
		except error as msg:
			cSock = None # Handle exception

		try:
			cSock.connect((host, port))
		except error as msg:
			cSock = None # Handle exception

		if cSock is None:
			print("Error: cannot open socket")
			sys.exit(1) # If the socket cannot be opened, quit the program.
		logFile = open('client_log.txt', "a")
		print("Type in a domain name to query, or 'q' to quit:")
		logFile.write(str(datetime.now()) + ": Type in a domain name to query, or 'q' to quit:\n")

		while 1:
			st = input() # Get input from users.
			if st == "":
				continue
			else:
				break
		logFile.write(str(datetime.now()) + ": " + st + "\n")
		if st == "q" or  st == "Q":
			cSock.close()
			logFile.write(str(datetime.now()) + ": Exit\n")
			logFile.close()
			sys.exit(1) # If input is "q" or "Q", quit the program.
		cSock.send(st.encode()) # Otherwise, send the input to server.
		data = cSock.recv(1024).decode() # Receive from server.
		print("Received:", data) # Print out the result.
		logFile.write(str(datetime.now()) + ": Received: " + data + '\n')
		logFile.close()		

main()
