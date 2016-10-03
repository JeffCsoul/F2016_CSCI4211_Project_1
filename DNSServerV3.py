# Fall 2016 CSci4211: Introduction to Computer Networks
# This program serves as the server of DNS query.
# Written in Python v3.

import sys, threading, os
from socket import *
from datetime import datetime

def main():

    serverhost_created = True
    logFile = open('server_log.txt', 'a')
    logFile.write(str(datetime.now()) + ": Server starts.\n")

    try:
        #create a socket object, SOCK_STREAM for TCP    
        sSock = socket(AF_INET, SOCK_STREAM)    
    except error as msg:
        # Handle exception
        serverhost_created = False
        print(msg)
        logFile.write(str(datetime.now()) + ": " + str(msg) + '\n')
        # print("DNSServer: Error in Creating the Socket.")

    try:
        #bind socket to the current address on port 5001
        sSock.bind(("localhost", 5001))
        #Listen on the given socket maximum number of connections queued is 20
        sSock.listen(20)
    except error as msg:
        # Handle exception
        serverhost_created = False
        print(msg)
        logFile.write(str(datetime.now()) + ": " + str(msg) + '\n')
        # print("DNSServer: Error in Binding as a Server Socket.")

    # If the socket cannot be opened, quit the program.
    if not serverhost_created:
        logFile.write(str(datetime.now()) + ": Server quit with error.\n")        
        logFile.close()
        quit()
    logFile.close()

    #start the control thread, which may terminate the program while encountering input "exit"
    monitor = threading.Thread(target=monitorQuit, args=[sSock])
    monitor.start()

    print("Server is listening...")

    while 1:
        #blocked until a remote machine connects to the local port 5001
        connectionSock, addr = sSock.accept()
        server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]])
        server.start()

def dnsQuery(connectionSock, srcAddress):
    #read line by line from the client host
    sSock = connectionSock
    data = sSock.recv(1024).decode()
    if data == "":
        sSock.close()
        return
    logFile = open('server_log.txt', 'a')
    logFile.write(str(datetime.now()) + ": Received valid query from " + str(srcAddress) +'\n')

    #Begin to check the query
    try:
        DNSCache = open("DNS_Mapping.txt", 'r')
    except error:
        newDNSCache = open("DNS_Mapping.txt", 'w')
        newDNSCache.close()
        DNSCache = open("DNS_Mapping.txt", 'r')
        logFile.write(str(datetime.now()) + ": No Local Cache. Created a New Cache File.\n")

    #If the query is "hangup" close the socket
    if data == "hangup":
        sSock.close()
        logFile.write(str(datetime.now()) + ": URL queried is 'hangup', close this socket.\n")  
        logFile.close()      
        return
    #Extract domain name.
    domainName = data
    logFile.write(str(datetime.now()) + ": URL queried is '" + domainName + "'\n")        
    IPanswer = ""    
    try:
        #First, check local DNS which is a file you created when the first query was successfully resolved(e.g. DNS_mapping.txt) 
        #If you find the result in this file, return the result with the appropriate format to the client   
        cacheDNSRecord = DNSCache.readline()
        recordFound = False
        while cacheDNSRecord != '' and not recordFound:
            cacheDNSRecord = cacheDNSRecord.split(':')
            recordDomainName = ':'.join(cacheDNSRecord[0:-1])
            if recordDomainName == domainName:
                recordFound = True
                if (cacheDNSRecord[-1].strip('\n') == "Host Not Found"):
                    IPanswer = "Host Not Found"
                else:
                    IPanswer = "Local DNS:" + domainName + ":" + cacheDNSRecord[-1].strip('\n')
            cacheDNSRecord = DNSCache.readline()
            #If the host name was not found in the local DNS file ,use the local machine DNS lookup and if found return it to the client
        DNSCache.close()
        if not recordFound:
            IPanswer = gethostbyname(domainName).strip('\n')
            DNSCache = open("DNS_Mapping.txt", "a")
            DNSCache.write(domainName + ':' + IPanswer + '\n')
            DNSCache.close()
            IPanswer = "Root DNS:" + domainName + ":" + IPanswer
            #also add the result to the local DNS file
    except:
        #If the host name was not found, return "Host Not Found to the client"
        IPanswer = "Host Not Found"
        DNSCache = open("DNS_Mapping.txt", "a")
        DNSCache.write(domainName + ':' + IPanswer + '\n')
        DNSCache.close()

    logFile.write(str(datetime.now()) + ": Message sent back: '" + IPanswer + "'\n")
    logFile.close()
    sSock.send(IPanswer.encode())
    sSock.close()
    #Close the server socket 

def monitorQuit(sSock):
    while 1:
        sentence = input()
        if sentence == "exit":
            #os.getpid() returns the parent thread id, which is the id of the main program
            #an hence terminate the main program
            logFile = open('server_log.txt', 'a')
            logFile.write(str(datetime.now()) + ": Exit\n")
            logFile.close()
            sSock.close()
            os.kill(os.getpid(),9)

main()
