import socket, sys
from .models import Quote
from transactions.models import Transactions

def get_quote(id, sym):
    # Get quote from quote server
    data = quoteClient(sym, id)
    elements = data.split(',')

    quoteResult = Quote(
        quote=float(elements[0]),
        stockSymbol=elements[1],
        userId=elements[2],
        timestamp=float(elements[3]),
        cryptokey=elements[4]
    )

    # Log quote server transaction
    transaction = Transactions(
        type="quoteServer",
        timestamp=float(elements[3]),
        server='QS',
        transactionNum=1, #TODO
        price=float(elements[0]),
        stockSymbol=elements[1],
        userId=elements[2],
        quoteServerTime=float(elements[3]),
        cryptoKey=elements[4]
    )
    transaction.save()

    return quoteResult

def quoteClient(sym, id):
    # Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket
    s.connect(('127.0.0.1',12345))

    # Send the user's query
    s.send('{},{}'.format(sym,id).encode())

    #Retrieving and parsing relevant data 
    data = s.recv(2048).decode()
    elements = data.split(',')

    quote = elements[0]
    stockSymbol = elements[1]
    userID = elements[2]
    timestamp = elements[3]
    cryptokey = elements[4]

    # close the connection, and the socket
    s.close()

    return data