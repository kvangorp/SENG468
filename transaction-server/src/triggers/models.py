from django.db import models

class Trigger(models.Model):
    stockSymbol = models.CharField(max_length=50)
    triggerPoint = models.FloatField()
    shares = models.IntegerField()
    isBuy = models.BooleanField()
