# Generated by Django 3.0.5 on 2021-03-20 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20210319_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttransaction',
            name='timestamp',
            field=models.BigIntegerField(default=1616202818697),
        ),
        migrations.AlterField(
            model_name='errorevent',
            name='timestamp',
            field=models.BigIntegerField(default=1616202818698),
        ),
        migrations.AlterField(
            model_name='quoteservertransaction',
            name='timestamp',
            field=models.BigIntegerField(default=1616202818694),
        ),
    ]
