from time import time
from django.db import models

class Account(models.Model):
    userId = models.CharField(max_length=50, unique=True, default='')
    # password = models.CharField(max_length=50, default = '')
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
    reserved =  models.FloatField(blank=True, default=0.0)
    #TODO: add constraint for userId and stockSymbol

class Trigger(models.Model):
    userId = models.CharField(max_length=50)
    stockSymbol = models.CharField(max_length=50)
    triggerPoint = models.FloatField(blank=True) #Null=Pending, Value=Committed
    amount = models.FloatField(blank=True)
    isBuy = models.BooleanField()