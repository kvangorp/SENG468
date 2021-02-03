from django.db import models

class Quote(models.Model):
    userId = models.CharField(max_length=50)
    stockSymbol = models.CharField(max_length=50)
    amount = models.IntegerField()
