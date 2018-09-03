# Generated by Django 2.0.5 on 2018-08-26 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0006_auto_20180819_2136'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostChatRestMessageCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='uuid',
            field=models.CharField(default='e59c6928ae9742f0ba77e9fe86d92ca8', max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='postchat',
            name='uuid',
            field=models.CharField(default='02b5014d646e453c83e24f6a3ae4a1e5', max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='uuid',
            field=models.CharField(default='71035280c6d14085a75a9c29e8daae1e', max_length=34, unique=True),
        ),
        migrations.AddField(
            model_name='postchatrestmessagecount',
            name='post',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='object.PostChat'),
        ),
    ]
