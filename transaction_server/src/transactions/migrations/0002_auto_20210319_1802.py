# Generated by Django 3.0.5 on 2021-03-20 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='accountTransaction', max_length=50)),
                ('timestamp', models.BigIntegerField(default=1616202156426)),
                ('server', models.CharField(default='TS', max_length=50)),
                ('transactionNum', models.IntegerField(blank=True)),
                ('action', models.CharField(blank=True, max_length=50)),
                ('username', models.CharField(blank=True, max_length=50)),
                ('funds', models.FloatField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ErrorEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='errorEvent', max_length=50)),
                ('timestamp', models.BigIntegerField(default=1616202156436)),
                ('server', models.CharField(default='TS', max_length=50)),
                ('transactionNum', models.IntegerField(blank=True)),
                ('command', models.CharField(blank=True, max_length=50)),
                ('username', models.CharField(blank=True, max_length=50)),
                ('errorMessage', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='QuoteServerTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='quoteServer', max_length=50)),
                ('timestamp', models.BigIntegerField(default=1616202156403)),
                ('server', models.CharField(default='QS', max_length=50)),
                ('transactionNum', models.IntegerField(blank=True)),
                ('price', models.FloatField(blank=True)),
                ('stockSymbol', models.CharField(blank=True, max_length=50)),
                ('username', models.CharField(blank=True, max_length=50)),
                ('quoteServerTime', models.BigIntegerField(default=0)),
                ('cryptokey', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserCommand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=50)),
                ('timestamp', models.BigIntegerField(blank=True)),
                ('server', models.CharField(blank=True, max_length=50)),
                ('transactionNum', models.IntegerField(blank=True)),
                ('command', models.CharField(blank=True, max_length=50)),
                ('username', models.CharField(blank=True, max_length=50)),
                ('stockSymbol', models.CharField(blank=True, max_length=50)),
                ('funds', models.FloatField(blank=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Transactions',
        ),
    ]
