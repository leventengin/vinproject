from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField, JSONField







DURUM = (
("0", 'Kapalı'),
("1", 'Sırada'),
("2", 'Serviste'),
("3", 'Dönüşte'),
("4", 'Sıradan Çıkmış'),
("5", 'SOS'),
)


KULLANICI_TIPI = (
("0", 'Motorcu'),
("1", 'Firma'),
("2", 'AnaFirma'),
("3", 'Merkez')
)

BILDIRIM_TIPI = (
("0", 'Sipariş var'),    
("1", 'Motorcu teslimatı kabul etmedi'),
("2", 'SOS'),
)


ISLEM_TIPI = (
("O", 'İşlem yapılmadı, başlangıç'), 
("1", 'Teslim edildi'),
("2", 'Ödeme alınamadı, teslim edildi'),
("3", 'Teslim edilemedi'),
("4", 'SOS'),
("5", 'SOS kaldır'),
)


TESLIM_EDILEMEDI = (
("0", 'Müşteri istemedi'),
("1", 'Müşteri yerinde yok'),
("2", 'Adresi bulamadım'),
("3", 'Diğer'),
)

ODEME_ALINAMADI = (
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

SOS_KALDIR = (
("0", 'Devam'),
("1", 'Ger, dön')
)

DEVICE_PLATFORM = (
("0", 'Android'),
("1", 'IOS'),
)




class User(AbstractUser):
    pass
    tipi = models.CharField(max_length=2, default="0")
    durum = models.CharField(max_length=2, default="0")
    aktif_firma = models.IntegerField(default=0)
    aktif_teslimat = models.IntegerField(default=0)
    aktif_islem = models.IntegerField(default=0)
    sira = models.IntegerField(default=0)
    enlem = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
    boylam = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
    aktif = models.BooleanField(default=True)
    tel_no = models.CharField(max_length=10, default="")
    pin = models.CharField(max_length=6, default="")
    kaydolunan_restoranlar = ArrayField(models.IntegerField(), blank=True, null=True)
    device_platform = models.CharField(max_length=1, choices=DEVICE_PLATFORM, default="0")
    device_id = models.CharField(max_length=40, default="0")
    pic_profile = models.ImageField(upload_to='pic_profile/%Y/%m/%d/',blank=True, null=True,)
    def __str__(self):
       return '%s-%s' % (self.first_name, self.last_name)




class AnaFirma(models.Model):
    anafirma_adi    = models.CharField(max_length=80)
    def __str__(self):
       return self.anafirma_adi


class Firma(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
    firma_adi = models.CharField(max_length=80)
    anafirma = models.ForeignKey(AnaFirma, null=True,blank=True, on_delete=models.PROTECT)
    tel_no = models.CharField(max_length=10, default="")
    pin = models.CharField(max_length=6, default="")
    allow_self_delivery = models.BooleanField(blank=False, default=False)
    kayitli_motorcular = ArrayField(models.IntegerField(), blank=True, null=True)
    adres = models.TextField()
    mahalle = models.CharField(max_length=80)
    ilce = models.CharField(max_length=80)
    il = models.CharField(max_length=80)
    enlem = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
    boylam = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
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
    kurye = models.ForeignKey(User, related_name='teslimat',  on_delete=models.PROTECT)
    firma = models.ForeignKey(Firma, related_name='teslimat_firma', on_delete=models.PROTECT)
    onay = models.BooleanField(default=True)
    adet = models.PositiveIntegerField(default=0)
    gecerli_adet = models.PositiveIntegerField(default=0)
    zaman = models.DateTimeField(auto_now=True)
    def __str__(self):
       return self.kurye.username




class IslemTeslimat(models.Model):
    teslimat = models.ForeignKey(Teslimat, related_name='teslimat', on_delete=models.PROTECT)
    islem_tipi = models.CharField(max_length=2, default="0")
    tel_no = models.CharField(max_length=10, default="")
    address = models.CharField(max_length=200)
    teslim_edilmedi_sebep = models.CharField(max_length=2, default="0")
    odeme_alinmadi_sebep = models.CharField(max_length=2, default="0")
    sos_sebep = models.CharField(max_length=2, default="0")
    sos_kaldir_sonuc = models.CharField(max_length=2, default="0")
    zaman = models.DateTimeField(auto_now=True)
    def __str__(self):
       return self.teslimat.kurye.username




class Bildirim(models.Model):
    tipi = models.CharField(max_length=2, default="0")
    receiver =  models.ForeignKey(User, related_name='receiver', on_delete=models.PROTECT)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.PROTECT)
    message = models.TextField(blank=True, null=True)
    viewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s-%s' % (self.sender, self.timestamp)



class Bahsis(models.Model):
    user = models.ForeignKey(User, related_name='bahsis', on_delete=models.PROTECT)
    zaman = models.DateTimeField(auto_now=True)
    miktar = models.DecimalField(max_digits=6, decimal_places=2,)
    def __str__(self):
       return self.user


class ArtiMotorcu(models.Model):
    user = models.ForeignKey(User, related_name='artimotorcu', on_delete=models.PROTECT)
    max_motorcu = models.PositiveIntegerField(default=0)
    gecen_motorcu_adedi = models.PositiveIntegerField(default=0)
    zaman = models.DateTimeField(auto_now=True)    
    def __str__(self):
       return self.user


class FaturaDetay(models.Model):
    user = models.ForeignKey(User, related_name='faturadetay', on_delete=models.PROTECT)
    yil = models.PositiveIntegerField(default=0)
    ay = models.PositiveIntegerField(default=0)
    max_motorcu = models.PositiveIntegerField(default=0)
    standart_ek = models.BooleanField(blank=True) 
    ek_kisi = models.PositiveIntegerField(default=0)
    ek_toplam = models.PositiveIntegerField(default=0) 
    standart_tutar = models.PositiveIntegerField(default=0) 
    ek_tutar = models.PositiveIntegerField(default=0) 
    def __str__(self):
        return '%s-%s-%s' % (self.user, self.yil, self.ay)


class FaturaToplam(models.Model):
    user = models.ForeignKey(User, related_name='faturatoplam', on_delete=models.PROTECT)
    yil = models.PositiveIntegerField(default=0)
    ay = models.PositiveIntegerField(default=0)
    odendi = models.BooleanField(blank=True) 
    tutar = models.PositiveIntegerField(default=0) 
    def __str__(self):
        return '%s-%s-%s' % (self.user, self.yil, self.ay)



class Fiyat(models.Model):
    max_motorcu = models.PositiveIntegerField(default=0)
    fiyat = models.PositiveIntegerField(default=0)
    def __str__(self):
        return '%s-%s' % (self.max_motorcu, self.fiyat)


class EkFiyat(models.Model):
    max_motorcu = models.ForeignKey(Fiyat, related_name='ek_fiyat', on_delete=models.PROTECT)    
    ek_motorcu = models.PositiveIntegerField(default=0)
    fiyat = models.PositiveIntegerField(default=0)
    def __str__(self):
        return '%s-%s-%s' % (self.max_motorcu, self.ek_motorcu,self.fiyat)


class Il(models.Model):
    il = models.CharField(max_length=80, default="İstanbul")
    def __str__(self):
        return '%s' % (self.il)

class Ilce(models.Model):
    il = models.ForeignKey(Il, related_name='ilce_il', on_delete=models.PROTECT)    
    ilce = models.CharField(max_length=80, default="Kadıköy")
    def __str__(self):
        return '%s-%s' % (self.il, self.ilce)

class Mahalle(models.Model):
    ilce = models.ForeignKey(Ilce, related_name='mahalle_ilce', on_delete=models.PROTECT)    
    mahalle = models.CharField(max_length=80, default="Fenerbahçe")
    def __str__(self):
        return '%s-%s-%s' % (self.ilce.il, self.ilce, self.mahalle)


class WSClient(models.Model):
    user = models.ForeignKey(User, related_name='wsclient', on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=200, default="")





