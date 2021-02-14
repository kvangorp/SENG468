from django.db import models

class Stock(models.Model):
    userId = models.CharField(max_length=50)
    stockSymbol = models.CharField(max_length=50, null=False)
    shares = models.FloatField(null=False)
    #TODO: add constraint for userId and stockSymbol