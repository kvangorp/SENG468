# Generated by Django 3.0.5 on 2021-02-20 00:24

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
                ('balance', models.FloatField(default=0.0)),
                ('pending', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.FloatField(default=0.0, max_length=50)),
                ('stockSymbol', models.CharField(default='', max_length=50)),
                ('userId', models.CharField(default='', max_length=50)),
                ('timestamp', models.BigIntegerField(default=0)),
                ('cryptokey', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(max_length=50)),
                ('stockSymbol', models.CharField(max_length=50)),
                ('shares', models.FloatField(default=0.0)),
                ('reserved', models.FloatField(blank=True, default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(max_length=50)),
                ('stockSymbol', models.CharField(max_length=50)),
                ('triggerPoint', models.FloatField(blank=True)),
                ('amount', models.FloatField(blank=True)),
                ('isBuy', models.BooleanField()),
            ],
        ),
    ]