# Generated by Django 2.2.4 on 2019-11-27 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kurye', '0002_auto_20191125_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default='', max_length=20)),
                ('created', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ticket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
