# Generated by Django 3.0.5 on 2021-02-10 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_stock_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='reserved',
            field=models.BooleanField(default=False),
        ),
    ]
