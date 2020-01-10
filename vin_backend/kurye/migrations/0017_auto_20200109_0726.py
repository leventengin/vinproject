# Generated by Django 2.2.4 on 2020-01-09 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kurye', '0016_auto_20200107_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pic_map',
            field=models.ImageField(blank=True, null=True, upload_to='pic_map/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='user',
            name='pic_map_abs_url',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]