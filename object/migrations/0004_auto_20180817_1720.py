# Generated by Django 2.0.5 on 2018-08-17 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0003_auto_20180813_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcommentlike',
            name='post_comment',
        ),
        migrations.RemoveField(
            model_name='postcommentlike',
            name='user',
        ),
        migrations.RemoveField(
            model_name='postcommentlikecount',
            name='post_comment',
        ),
        migrations.AddField(
            model_name='postchatrestmessage',
            name='text',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='postcomment',
            name='text',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='uuid',
            field=models.CharField(default='32bfdea208844478b1f38c90c9967826', max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='postchat',
            name='uuid',
            field=models.CharField(default='846c62044858401a8e59d4de3f5a19a9', max_length=34, unique=True),
        ),
        migrations.DeleteModel(
            name='PostCommentLike',
        ),
        migrations.DeleteModel(
            name='PostCommentLikeCount',
        ),
    ]
