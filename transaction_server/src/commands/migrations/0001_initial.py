# Generated by Django 3.0.5 on 2021-02-16 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(default='', max_length=50, unique=True)),
                ('password', models.CharField(default='', max_length=50)),
                ('balance', models.FloatField(default=0.0)),
                ('pending', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.FloatField(default='', max_length=50)),
                ('stockSymbol', models.CharField(default='', max_length=50)),
                ('userId', models.CharField(default='', max_length=50)),
                ('timestamp', models.FloatField(default='', max_length=50)),
                ('cryptokey', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(max_length=50)),
                ('stockSymbol', models.CharField(max_length=50)),
                ('shares', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=50)),
                ('userId', models.CharField(blank=True, max_length=50)),
                ('stockSymbol', models.CharField(blank=True, max_length=50)),
                ('userCommand', models.CharField(blank=True, max_length=50)),
                ('timestamp', models.FloatField(default=1613434298.91615)),
                ('quoteServerTime', models.FloatField(blank=True)),
                ('cryptoKey', models.CharField(blank=True, max_length=50)),
                ('price', models.FloatField(blank=True)),
                ('server', models.CharField(blank=True, max_length=50)),
                ('transactionNum', models.IntegerField(blank=True)),
                ('amount', models.FloatField(blank=True)),
                ('systemEvent', models.CharField(blank=True, max_length=50)),
                ('debugEvent', models.CharField(blank=True, max_length=50)),
                ('errorEvent', models.CharField(blank=True, max_length=50)),
                ('debugMessage', models.CharField(blank=True, max_length=50)),
                ('fileName', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(max_length=50)),
                ('stockSymbol', models.CharField(max_length=50)),
                ('triggerPoint', models.FloatField(blank=True)),
                ('shares', models.IntegerField()),
                ('isBuy', models.BooleanField()),
            ],
        ),
    ]
