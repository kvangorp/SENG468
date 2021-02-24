import random
import sys
import string
import time
from socket import *


# Create a UDP socket 
serverSocket = socket(AF_INET, SOCK_STREAM)



# Assign IP address and port number to socket
host = 'quote_server'
port = 4444
serverSocket.bind((host,port))
serverSocket.listen(5)
print('Ready to serve... Send quote information')

while True:
	# Receive the client packet along with the address it is coming from 
    try:
        clientsocket, address = serverSocket.accept()
        print("...Connected from: "),address

        message = clientsocket.recvfrom(2028)
        print(message[0])
        request = message[0].decode().split(',') 

        # Generate random number in the range of 1 to 10 and if rand is less is than 4, we consider the packet lost and tell the client to retransmit
        quote = round(random.uniform(1.0,5.0),2)
        stocksymbol = request[0]
        userID = request[1]
        timestamp = int(time.time())
        letters = string.ascii_lowercase
        cryptokey = ''.join(random.choice(letters) for i in range(10))

        quoteResp = '{},{},{},{},{}'.format(quote,stocksymbol,userID,timestamp,cryptokey)
        clientsocket.sendto(quoteResp.encode(),address)
        clientsocket.close()
    except IOError:
        #Send response message for file not found
        clientsocket.send('Error') 

        #Close client socket
        clientsocket.close()

serverSocket.close()
sys.exit()