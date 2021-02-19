from django.db import models
from time import time

class Transactions(models.Model):
    type = models.CharField(max_length=50, blank=True)
    userId = models.CharField(max_length=50, blank=True)
    stockSymbol = models.CharField(max_length=50, blank=True)
    userCommand = models.CharField(max_length=50, blank=True)
    timestamp = models.BigIntegerField(default=0)
    quoteServerTime = models.BigIntegerField(default=0)
    cryptoKey = models.CharField(max_length=50, blank=True)
    price = models.FloatField(blank=True)
    server = models.CharField(max_length=50, blank=True)
    transactionNum = models.IntegerField(blank=True)
    amount = models.FloatField(blank=True)
    systemEvent = models.CharField(max_length=50, blank=True)
    debugEvent = models.CharField(max_length=50, blank=True)
    errorEvent = models.CharField(max_length=50, blank=True)
    debugMessage = models.CharField(max_length=50, blank=True)
    fileName = models.CharField(max_length=50, blank=True)
