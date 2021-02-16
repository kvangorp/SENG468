from time import time
from django.db import models

class Account(models.Model):
    userId = models.CharField(max_length=50, unique=True, default='')
    password = models.CharField(max_length=50, default = '')
    balance = models.FloatField(default = 0.0)
    pending = models.FloatField(default = 0.0)

class Quote(models.Model):
    quote = models.FloatField(max_length=50,default='')
    stockSymbol = models.CharField(max_length=50,default='')
    userId = models.CharField(max_length=50, default='')
    timestamp = models.FloatField(max_length=50,default='')
    cryptokey = models.CharField(max_length=50,default='')

class Stock(models.Model):
    userId = models.CharField(max_length=50)
    stockSymbol = models.CharField(max_length=50, null=False)
    shares = models.FloatField(null=False)
    #TODO: add constraint for userId and stockSymbol

class Trigger(models.Model):
    userId = models.CharField(max_length=50)
    stockSymbol = models.CharField(max_length=50)
    triggerPoint = models.FloatField(blank=True)
    shares = models.IntegerField()
    isBuy = models.BooleanField()

class Transactions(models.Model):
    type = models.CharField(max_length=50, blank=True)
    userId = models.CharField(max_length=50, blank=True)
    stockSymbol = models.CharField(max_length=50, blank=True)
    userCommand = models.CharField(max_length=50, blank=True)
    timestamp = models.FloatField(default=time())
    quoteServerTime = models.FloatField(blank=True)
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
