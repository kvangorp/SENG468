from django.db import models
from time import time

class QuoteServerTransaction(models.Model):
    type = models.CharField(max_length=50, default="quoteServer")
    timestamp = models.BigIntegerField(default=int(time()*1000))
    server = models.CharField(max_length=50, default="QS")
    transactionNum = models.IntegerField(blank=True)
    price = models.FloatField(blank=True)
    stockSymbol = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, blank=True)
    quoteServerTime = models.BigIntegerField(default=0)
    cryptokey = models.CharField(max_length=50, blank=True)

class AccountTransaction(models.Model):
    type = models.CharField(max_length=50, default="accountTransaction")
    timestamp = models.BigIntegerField(default=int(time()*1000))
    server = models.CharField(max_length=50, default="TS")
    transactionNum = models.IntegerField(blank=True)
    action = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, blank=True)
    funds = models.FloatField(blank=True)

class ErrorEvent(models.Model):
    type = models.CharField(max_length=50, default="errorEvent")
    timestamp = models.BigIntegerField(default=int(time()*1000))
    server = models.CharField(max_length=50, default="TS")
    transactionNum = models.IntegerField(blank=True)
    command = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, blank=True)
    errorMessage = models.CharField(max_length=50, blank=True)

class UserCommand(models.Model):
    type = models.CharField(max_length=50, blank=True)
    timestamp = models.BigIntegerField(blank=True)
    server = models.CharField(max_length=50, blank=True)
    transactionNum = models.IntegerField(blank=True)
    command = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, blank=True)
    stockSymbol = models.CharField(max_length=50, blank=True)
    funds = models.FloatField(blank=True)

