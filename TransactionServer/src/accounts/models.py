from django.db import models

class Account(models.Model):
    userId = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    balance = models.FloatField()
