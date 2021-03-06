# Generated by Django 2.0 on 2020-08-02 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FiveTaskModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('lost', '失物招领'), ('pick', '拾取'), ('repair', '报修'), ('run', '一起运动'), ('paotui', '跑腿')], default='lost', max_length=60, verbose_name='类别')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('addr', models.CharField(max_length=255, verbose_name='地址')),
                ('name', models.CharField(max_length=60, null=True, verbose_name='姓名_时间_薪资')),
                ('telephone', models.CharField(max_length=60, null=True, verbose_name='手机号码')),
                ('img', models.ImageField(blank=True, null=True, upload_to='lp/images/%y/%d/e3fddbfa6b8f4a6a890adec75b460b1a', verbose_name='物品图片')),
                ('desc', models.TextField(null=True, verbose_name='物品描述')),
                ('isMe', models.BooleanField(default=False, verbose_name='我的任务')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('nums', models.IntegerField(default=0, verbose_name='报名人数')),
            ],
            options={
                'verbose_name': '丢失拾取报修跑腿运动',
                'verbose_name_plural': '丢失拾取报修跑腿运动',
                'db_table': 'fivetask',
            },
        ),
    ]
