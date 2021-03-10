import socket, sys, os
import redis
from time import time
from django.conf import settings
from transactions.models import Transactions
from .transactionsLogger import log_quote_server_transaction
redis_instance = redis.StrictRedis(charset="utf-8", decode_responses=True, host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
EXPIRY_SECS = 60

def get_quote(username, stockSymbol, transactionNum=1, isSysEvent=False):
    res = redis_instance.hgetall(stockSymbol)
    if not res:
        # If quote is not in redis database
        # Get quote from quote server
        data = quoteClient(stockSymbol, username)
        elements = data.split(',')

        # Add quote to redis database
        quote = {
            "quote": float(elements[0]),
            "stockSymbol": stockSymbol,
            "userId": username,
            "timestamp": int(elements[3]),
            "cryptoKey": elements[4],
        }
        redis_instance.hmset(stockSymbol, quote)
        redis_instance.expire(stockSymbol, EXPIRY_SECS)
        res = redis_instance.hgetall(stockSymbol)

        # Log quote server transaction
        log_quote_server_transaction(transactionNum, res["quote"], res["stockSymbol"], username, res["timestamp"], res["cryptoKey"])
        print(res)

    return float(res["quote"])

def quoteClient(stockSymbol, username):
    # Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket
    s.connect((os.environ['quoteServerHost'],4444))

    request = f'{stockSymbol},{username}\n'.encode()
    print(request)
    # Send the user's query
    s.send(request)
    print('sent')
    #Retrieving and parsing relevant data 
    data = s.recv(2048).decode()
    elements = data.split(',')
    print('received')
    quote = elements[0]
    stockSymbol = elements[1]
    userID = elements[2]
    timestamp = int(elements[3])
    cryptokey = elements[4]

    # close the connection, and the socket
    s.close()

    return data
