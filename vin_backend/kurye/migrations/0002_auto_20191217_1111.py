# Generated by Django 2.2.4 on 2019-12-17 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kurye', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='sos_reason',
        ),
        migrations.RemoveField(
            model_name='order',
            name='sos_result',
        ),
    ]