from django.db import models

class Account(models.Model):
    userId = models.CharField(max_length=50, unique=True)
    password = models.CharField(min=6, max=50)
    balance = models.FloatField()
