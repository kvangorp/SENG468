from django.db import models

class Account(models.Model):
    userId = models.CharField(max_length=50, unique=True, default='A')
    password = models.CharField(max_length=50, default = 'B')
    balance = models.FloatField(default = 0.0)
    pending = models.FloatField(default = 0.0)
