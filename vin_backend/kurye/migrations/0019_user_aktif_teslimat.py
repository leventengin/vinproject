# Generated by Django 2.2.4 on 2019-12-12 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kurye', '0018_auto_20191211_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='aktif_teslimat',
            field=models.IntegerField(default=0),
        ),
    ]