# Generated by Django 2.0.5 on 2018-08-17 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0004_auto_20180817_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='uuid',
            field=models.CharField(default='95636cdc44f4484985816c0a21d7bc06', max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='uuid',
            field=models.CharField(default='6cd236852cfd4c63a05502979f10f379', max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='postchat',
            name='uuid',
            field=models.CharField(default='b00f9492fb0b4c4ca63272fc842e3871', max_length=34, unique=True),
        ),
    ]
