# Generated by Django 2.2.4 on 2019-12-14 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kurye', '0028_auto_20191213_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teslimat',
            name='onay',
            field=models.BooleanField(default=False),
        ),
    ]