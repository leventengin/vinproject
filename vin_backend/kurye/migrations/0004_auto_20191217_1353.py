# Generated by Django 2.2.4 on 2019-12-17 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kurye', '0003_auto_20191217_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='courier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courier', to='kurye.Courier'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='restaurant', to='kurye.Restaurant'),
        ),
    ]
