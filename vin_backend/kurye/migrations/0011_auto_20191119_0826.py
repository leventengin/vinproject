# Generated by Django 2.2.4 on 2019-11-19 08:26

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kurye', '0010_auto_20191119_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firma',
            name='kayitli_motorcular',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
