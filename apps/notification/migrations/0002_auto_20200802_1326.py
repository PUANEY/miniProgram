# Generated by Django 2.0 on 2020-08-02 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifymodel',
            name='is_read',
        ),
        migrations.AlterField(
            model_name='notifymodel',
            name='notify_type',
            field=models.IntegerField(choices=[(0, '活动消息'), (1, '点赞'), (2, '评论'), (3, '官方消息')], default=0, help_text='消息类型', verbose_name='消息类型'),
        ),
    ]
