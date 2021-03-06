# Generated by Django 2.0.5 on 2018-09-02 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0009_auto_20180827_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='uuid',
            field=models.CharField(default='cb68abac27fe4357835831f390ad4703', max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='postchat',
            name='uuid',
            field=models.CharField(default='2e3f5b10ec85491091f01175d8adf39a', max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='postchatrestmessage',
            name='uuid',
            field=models.CharField(default='5af4e49b7d384445ab64381261449908', max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='postchatrestmessagelikecount',
            name='post_chat_rest_message',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='object.PostChatRestMessage'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='uuid',
            field=models.CharField(default='fce396f4d2484acb98a1ff55f4b71b78', max_length=34, unique=True),
        ),
    ]
