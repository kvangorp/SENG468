import socket, sys, os
import redis, json
from time import time
from django.conf import settings
from transactions.models import QuoteServerTransaction, AccountTransaction, ErrorEvent

def log_quote_server_transaction(transactionNum, price, stockSymbol, username, quoteServerTime, cryptokey):
    transaction = QuoteServerTransaction(
        transactionNum = transactionNum, 
        price = price,
        stockSymbol = stockSymbol,
        username = username,
        quoteServerTime = quoteServerTime,
        cryptokey = cryptokey
    )
    transaction.save()

def log_account_transaction(transactionNum, action, username, funds):
    transaction = AccountTransaction(
        transactionNum = transactionNum,
        action = action,
        username = username,
        funds = funds
    )
    transaction.save()

def log_error_event(transactionNum, command, username, errorMessage):
    transaction = ErrorEvent(
        transactionNum = transactionNum,
        command = command,
        username = username,
        errorMessage = errorMessage
    )
    transaction.save()
