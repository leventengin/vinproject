# Generated by Django 2.2.4 on 2019-11-07 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kurye', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grup_adi', models.CharField(max_length=80)),
            ],
        ),
    ]
