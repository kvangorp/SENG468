from django.db import models

class Account(models.Model):
    userId = models.CharField(max_length=50, unique=True, default='')
    password = models.CharField(max_length=50, default = '')
    balance = models.FloatField(default = 0.0)
    pending = models.FloatField(default = 0.0)
