from django.db import models

class Trigger(models.Model):
    userId = models.CharField(max_length=50)
    stockSymbol = models.CharField(max_length=50)
    triggerPoint = models.FloatField(blank=True)
    shares = models.IntegerField()
    isBuy = models.BooleanField()
