from time import time
from django.db import models

class Account(models.Model):
    userId = models.CharField(max_length=50, unique=True, default='')
    # password = models.CharField(max_length=50, default = '')
    balance = models.FloatField(default = 0.0)
    pending = models.FloatField(default = 0.0)

class Quote(models.Model):
    quote = models.FloatField(max_length=50,default=0.0)
    stockSymbol = models.CharField(max_length=50,default='')
    userId = models.CharField(max_length=50, default='')
    timestamp = models.BigIntegerField(default=0)
    cryptokey = models.CharField(max_length=50,default='')

class Stock(models.Model):
    userId = models.CharField(max_length=50)
    stockSymbol = models.CharField(max_length=50, null=False)
    shares = models.FloatField(null=False, default=0.0)
    reserved =  models.FloatField(blank=True, default=0.0)
    #TODO: add constraint for userId and stockSymbol

class PendingBuy(models.Model):
    timestamp = models.BigIntegerField(default=0)
    userId = models.CharField(max_length=50)
    stockSymbol = models.CharField(max_length=50, null=False)
    dollarAmount = models.FloatField(default=0.0)

class PendingSell(models.Model):
    timestamp = models.BigIntegerField(default=0)
    userId = models.CharField(max_length=50)
    stockSymbol = models.CharField(max_length=50, null=False)
    dollarAmount = models.FloatField(default=0.0)
    shares = models.FloatField(default=0.0)

class Trigger(models.Model):
    userId = models.CharField(max_length=50)
    stockSymbol = models.CharField(max_length=50)
    triggerPoint = models.FloatField(blank=True) #Null=Pending, Value=Committed
    amount = models.FloatField(blank=True) # Dollar amount for buy, shares for Sell
    isBuy = models.BooleanField()
