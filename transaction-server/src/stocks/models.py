from django.db import models

class Stock(models.Model):
    stockSymbol = models.CharField(max_length=50)
    shares = models.IntegerField()
