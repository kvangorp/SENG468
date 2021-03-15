import socket, sys, os
import redis, json
from time import time
from django.conf import settings
redis_instance = redis.StrictRedis(charset="utf-8", decode_responses=True, host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)

def log_quote_server_transaction(transactionNum, price, stockSymbol, username, quoteServerTime, cryptokey):
    transaction = {
        "type": "quoteServer",
        "timestamp": int(time()*1000),
        "server": "QS",
        "transactionNum": transactionNum, 
        "price": price,
        "stockSymbol": stockSymbol,
        "username": username,
        "quoteServerTime": quoteServerTime,
        "cryptokey": cryptokey
    }
    hash_key = str(transaction["transactionNum"])
    redis_instance.sadd(hash_key, json.dumps(transaction))

def log_account_transaction(transactionNum, action, username, funds):
    transaction = {
        "type": "accountTransaction",
        "timestamp": int(time()*1000),
        "server": 'TS',
        "transactionNum": transactionNum,
        "action": action,
        "username": username,
        "funds": funds
    }
    hash_key = str(transaction["transactionNum"])
    redis_instance.sadd(hash_key, json.dumps(transaction))

def log_error_event(transactionNum, command, username, errorMessage):
    transaction = {
        "type": "errorEvent",
        "timestamp": int(time()*1000),
        "server":'TS',
        "transactionNum": transactionNum,
        "command": command,
        "username": username,
        "errorMessage": errorMessage
    }
    hash_key = str(transaction["transactionNum"])
    redis_instance.sadd(hash_key, json.dumps(transaction))
