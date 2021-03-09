import socket, sys, os
import redis
from time import time
from django.conf import settings
from .models import Quote
from transactions.models import Transactions
redis_instance = redis.StrictRedis(charset="utf-8", decode_responses=True, host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
EXPIRY_SECS = 60

def get_quote(id, sym,transactionNum=1,isSysEvent=False):
    res = redis_instance.hgetall(sym)
    if not res:
        # If quote is not in redis database
        # Get quote from quote server
        data = quoteClient(sym, id)
        elements = data.split(',')
        stockSymbol = elements[1]

        # Add quote to redis database
        quote = {
            "quote": float(elements[0]),
            "stockSymbol": stockSymbol,
            "userId": elements[2],
            "timestamp": int(elements[3]),
            "cryptoKey": elements[4],
        }
        redis_instance.hmset(stockSymbol, quote)
        redis_instance.expire(stockSymbol, EXPIRY_SECS)
        res = redis_instance.hgetall(sym)
    print(res)

    # Log quote server transaction
    transaction = Transactions(
        type="quoteServer",
        timestamp=int(time())*1000,
        server='QS',
        transactionNum=transactionNum, 
        price=res["quote"],
        stockSymbol=res["stockSymbol"],
        userId=id,
        quoteServerTime=res["timestamp"],
        cryptoKey=res["cryptoKey"]
    )
    transaction.save()

    return float(res["quote"])

def quoteClient(sym, id):
    # Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket
    s.connect((os.environ['quoteServerHost'],4444))

    request = f'{sym},{id}\n'.encode()
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
