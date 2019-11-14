from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField


DURUM = (
("0", 'Kapalı'),
("1", 'Dönüyor'),
("2", 'Gidiyor'),
("3", 'Sırada'),
("4", 'Sıradan Çıkmış'),
("5", 'SOS'),
)

KULLANICI_TIPI = (
("0", 'Motorcu'),
("1", 'Firma'),
("2", 'AnaFirma'),
)

BILDIRIM_TIPI = (
("0", 'SOS'),
)


TESLIM_EDILMEDI = (
("0", 'Müşteri istemedi'),
("1", 'Müşteri yerinde yok'),
("2", 'Adresi bulamadım'),
("3", 'Diğer'),
)


ODEME_ALINMADI = (
("0", 'POS kaynaklı'),
("1", 'Para üstü yok'),
("2", 'Müşteride para yok'),
("3", 'Diğer'),
)


SOS_SEBEP = (
("0", 'Kaza'),
("1", 'Arıza'),
("2", 'Benzin'),
("3", 'Çevirme'),
("4", 'Diğer'),
)



class User(AbstractUser):
    pass
    tipi = models.CharField(max_length=2, default="0")
    durum = models.CharField(max_length=2, default="0")
    enlem = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
    boylam = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
    aktif = models.BooleanField(default=True)
    pic_profile = models.ImageField(upload_to='pic_profile/%Y/%m/%d/',blank=True, null=True,)
    def __str__(self):
       return '%s-%s' % (self.first_name, self.last_name)


class AnaFirma(models.Model):
    anafirma_adi    = models.CharField(max_length=80)
    def __str__(self):
       return self.anafirma_adi


class Firma(models.Model):
    firma_adi = models.CharField(max_length=80)
    anafirma = models.ForeignKey(AnaFirma, null=True,blank=True, on_delete=models.PROTECT)
    adres = models.TextField()
    mahalle = models.CharField(max_length=80)
    ilce = models.CharField(max_length=80)
    il = models.CharField(max_length=80)
    enlem = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
    boylam = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
    motorcular = ArrayField( models.IntegerField())
    belge_1 = models.ImageField(upload_to='belge_1/%Y/%m/%d/',blank=True, null=True,)
    belge_2 = models.ImageField(upload_to='belge_2/%Y/%m/%d/',blank=True, null=True,)
    belge_3 = models.ImageField(upload_to='belge_3/%Y/%m/%d/',blank=True, null=True,)
    belge_4 = models.ImageField(upload_to='belge_4/%Y/%m/%d/',blank=True, null=True,)
    belge_5 = models.ImageField(upload_to='belge_5/%Y/%m/%d/',blank=True, null=True,)
    belge_6 = models.ImageField(upload_to='belge_6/%Y/%m/%d/',blank=True, null=True,)
    belge_7 = models.ImageField(upload_to='belge_7/%Y/%m/%d/',blank=True, null=True,)
    belge_8 = models.ImageField(upload_to='belge_8/%Y/%m/%d/',blank=True, null=True,)
    def __str__(self):
       return self.firma_adi



class Teslimat(models.Model):
    user = models.ForeignKey(User, related_name='teslimat', on_delete=models.PROTECT)
    firma = models.ForeignKey(Firma, related_name='teslimat_firma', on_delete=models.PROTECT)
    zaman = models.DateTimeField(auto_now=True)
    teslim_edildi = models.BooleanField(blank=True)
    odeme_alindi = models.BooleanField(blank=True)
    teslim_edilmedi_sebep = models.CharField(max_length=2, default="0")
    odeme_alinmadi_sebep = models.CharField(max_length=2, default="0")
    odeme_alinmadi_sebep_adi = models.CharField(max_length=20,)
    odeme_alinmadi_sebep_soyadi = models.CharField(max_length=20)
    odeme_alinmadi_sebep_tel = models.CharField(max_length=12)
    odeme_alinmadi_sebep_adres = models.CharField(max_length=60)
    def __str__(self):
       return self.user


class Islemler(models.Model):
    user = models.ForeignKey(User, related_name='islem', on_delete=models.PROTECT)
    firma = models.ForeignKey(Firma, related_name='islem_firma', on_delete=models.PROTECT)
    zaman = models.DateTimeField(auto_now=True)
    islem = models.CharField(max_length=2, default="0")
    sos_sebep = models.CharField(max_length=2, default="0")
    def __str__(self):
       return self.user


class Bildirim(models.Model):
    tipi = models.CharField(max_length=2, default="0")
    user =  models.ForeignKey(User, related_name='bildirim', on_delete=models.PROTECT)
    viewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s-%s' % (self.user, self.timestamp)


class Bahsis(models.Model):
    user = models.ForeignKey(User, related_name='bahsis', on_delete=models.PROTECT)
    zaman = models.DateTimeField(auto_now=True)
    miktar = models.DecimalField(max_digits=6, decimal_places=2,)
    def __str__(self):
       return self.user
