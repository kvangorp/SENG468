from django.db import models

class Quote(models.Model):
    stockSymbol = models.CharField(max_length=50)
    amount = models.IntegerField()
