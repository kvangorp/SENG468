# Generated by Django 3.0.5 on 2021-02-15 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20210214_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='timestamp',
            field=models.FloatField(default=1613349151.368143),
        ),
    ]
