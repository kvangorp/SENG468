from django.db import models

class Quote(models.Model):
    quote = models.FloatField()
    stockSymbol = models.CharField(max_length=50)
    userId = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    cryptokey = models.CharField(max_length=50)
