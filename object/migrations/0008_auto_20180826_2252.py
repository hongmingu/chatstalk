# Generated by Django 2.0.5 on 2018-08-26 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0007_auto_20180826_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='postchatrestmessage',
            name='uuid',
            field=models.CharField(default='2035ff4ffaba4c44b5ec14227fa348e4', max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='uuid',
            field=models.CharField(default='32004092f78d4b3f8ed112aa240c109c', max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='postchat',
            name='uuid',
            field=models.CharField(default='ae20fbfdf1aa4d289282aab4a453ad5c', max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='uuid',
            field=models.CharField(default='ee76cfdf20314adfb19b387042ca071b', max_length=34, unique=True),
        ),
    ]
