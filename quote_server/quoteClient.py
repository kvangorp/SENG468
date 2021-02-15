import socket, sys

# Print info for the user
print("\nEnter: StockSYM, userid");
print("  Invalid entry will return 'NA' for userid.");
print("  Returns: quote,sym,userid,timestamp,cryptokey\n");

# Get a line of text from the user
#fromUser = sys.stdin.readline().encode();

# Create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket
s.connect(('127.0.0.1',12345))
# Send the user's query
s.send('S,oY01WVirLr'.encode())
#s.send(fromUser)


#Retrieving and parsing relevant data 
data = s.recv(2048).decode()
elements = data.split(',')
 
quote = elements[0]
stockSymbol = elements[1]
userID = elements[2]
timestamp = elements[3]
cryptokey = elements[4]
print(data)

# close the connection, and the socket
s.close()