# Generated by Django 2.0.7 on 2018-07-12 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burritobot', '0003_auto_20180711_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='command',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='command',
            name='response',
            field=models.CharField(max_length=20000),
        ),
    ]