import time
from django.db import models

class Quote(models.Model):
    quote = models.FloatField(max_length=50,default='')
    stockSymbol = models.CharField(max_length=50,default='')
    userId = models.CharField(max_length=50, default='')
    timestamp = models.FloatField(max_length=50,default='')
    cryptokey = models.CharField(max_length=50,default='')
