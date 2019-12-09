# Generated by Django 2.2.4 on 2019-12-08 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kurye', '0010_auto_20191205_0715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='islemteslimat',
            name='odeme_alinmadi_sebep_adi',
        ),
        migrations.RemoveField(
            model_name='islemteslimat',
            name='odeme_alinmadi_sebep_adres',
        ),
        migrations.RemoveField(
            model_name='islemteslimat',
            name='odeme_alinmadi_sebep_soyadi',
        ),
        migrations.RemoveField(
            model_name='islemteslimat',
            name='odeme_alinmadi_sebep_tel',
        ),
        migrations.RemoveField(
            model_name='islemteslimat',
            name='sos_kaldir_sebep',
        ),
        migrations.RemoveField(
            model_name='islemteslimat',
            name='sos_sebep',
        ),
        migrations.AddField(
            model_name='islemteslimat',
            name='address',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teslimat',
            name='sos_kaldir_sebep',
            field=models.CharField(default='0', max_length=2),
        ),
        migrations.AddField(
            model_name='teslimat',
            name='sos_sebep',
            field=models.CharField(default='0', max_length=2),
        ),
    ]
