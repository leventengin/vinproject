# Generated by Django 2.2.4 on 2019-12-11 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kurye', '0016_auto_20191210_0700'),
    ]

    operations = [
        migrations.RenameField(
            model_name='firma',
            old_name='user',
            new_name='restoran',
        ),
        migrations.AlterField(
            model_name='teslimat',
            name='firma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teslimat_firma', to='kurye.Firma', to_field='user'),
        ),
    ]
