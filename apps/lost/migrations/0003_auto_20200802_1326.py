# Generated by Django 2.0 on 2020-08-02 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lost', '0002_auto_20200802_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fivetaskmodel',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='lp/images/%y/%d/1a746781e5414445a753848aac16381f', verbose_name='物品图片'),
        ),
    ]
