# Generated by Django 3.0.5 on 2021-03-20 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_auto_20210319_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttransaction',
            name='timestamp',
            field=models.BigIntegerField(default=1616202160274),
        ),
        migrations.AlterField(
            model_name='errorevent',
            name='timestamp',
            field=models.BigIntegerField(default=1616202160295),
        ),
        migrations.AlterField(
            model_name='quoteservertransaction',
            name='timestamp',
            field=models.BigIntegerField(default=1616202160273),
        ),
    ]
