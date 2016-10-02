# CSCI4211_Project_1
Server:
	Run:
		Using 'python3 DNSServerV3.py' to start the server.
		Enter 'exit' to kill the server processor.
Client:
	Run:
		Using 'python3 DNSClientV3.py' to start the client.
		Enter 'exit' to exit.

The function main() is to create socket for listening to the client and thread a processor to call dnsQuery() when it received a query.

The function dnsQuery() is to parse the query and send back the result of the query. The function also can handle the situation that the query includes symbol ':'. The function would return the IP in cache if the domain record already exists in the cache. Otherwise it will send back the ip getting from local machine DNS lookup and cached the record for future use.

The function monitorQuit() is to monitor the commands entered. If 'exit' appears, it would halt the program.