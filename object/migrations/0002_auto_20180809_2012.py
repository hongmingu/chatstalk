# Generated by Django 2.0.5 on 2018-08-09 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='uuid',
            field=models.CharField(default='7e2286044d2a433ba6d11bcddb3583cb', max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='postchat',
            name='uuid',
            field=models.CharField(default='1e6a00e9eda4431aa855919f35a28bea', max_length=34, unique=True),
        ),
    ]
