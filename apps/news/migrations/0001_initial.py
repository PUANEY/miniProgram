# Generated by Django 2.0 on 2020-08-02 11:07

import DjangoUeditor.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='banner', verbose_name='轮播图片')),
                ('index', models.IntegerField(default=0, verbose_name='轮播顺序')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '轮播新闻',
                'verbose_name_plural': '轮播新闻',
            },
        ),
        migrations.CreateModel(
            name='NewsComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=300, verbose_name='新闻评论内容')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
            ],
            options={
                'verbose_name': '新闻评论',
                'verbose_name_plural': '新闻评论',
                'db_table': 'news_comments',
            },
        ),
        migrations.CreateModel(
            name='NewsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='新闻标题')),
                ('desc', models.TextField(verbose_name='简介')),
                ('content', DjangoUeditor.models.UEditorField(default='', verbose_name='正文')),
                ('image', models.ImageField(upload_to='newsImages', verbose_name='展示图片')),
                ('visit', models.IntegerField(default=0, verbose_name='浏览量')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
            ],
            options={
                'verbose_name': '新闻信息',
                'verbose_name_plural': '新闻信息',
                'db_table': 'news_info',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='标签')),
            ],
            options={
                'verbose_name': '新闻标签',
                'verbose_name_plural': '新闻标签',
                'db_table': 'news_tag',
            },
        ),
    ]
