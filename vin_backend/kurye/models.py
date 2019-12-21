from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField, JSONField
import requests
from django.contrib.auth import get_user_model
from push_notifications.models import APNSDevice, GCMDevice
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer





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

SOS_SONUC = (
("0", 'Devam'),
("1", 'Geri dön')
)

DEVICE_PLATFORM = (
("0", 'Android'),
("1", 'IOS'),
)




class User(AbstractUser):
    pass
    user_type = models.CharField(max_length=2, default="0")
    pic_profile = models.ImageField(upload_to='pic_profile/%Y/%m/%d/',blank=True, null=True,)
    pic_profile_abs_url = models.TextField(blank=True, null=True, default=None)
    def __str__(self):
       return '%s-%s' % (self.first_name, self.last_name)




class Company(models.Model):
    user_company = models.OneToOneField(User, related_name="user_company", on_delete=models.PROTECT, primary_key=True)    
    name    = models.CharField(max_length=80)
    def __str__(self):
       return self.name


class Restaurant(models.Model):
    user_restaurant = models.OneToOneField(User, related_name="user_restaurant", on_delete=models.PROTECT, primary_key=True)
    name = models.CharField(max_length=80)
    company = models.ForeignKey(Company, null=True,blank=True, on_delete=models.PROTECT)
    tel_no = models.CharField(max_length=10, default="")
    second_tel = models.CharField(max_length=10, default="")
    allow_self_delivery = models.BooleanField(blank=False, default=False)
    registered_couriers = models.ManyToManyField('Courier', blank=True)
    adress = models.TextField()
    district = models.CharField(max_length=80)
    town = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    latitude = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
    longitude = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
    doc_1 = models.ImageField(upload_to='belge_1/%Y/%m/%d/',blank=True, null=True,)
    doc_2 = models.ImageField(upload_to='belge_2/%Y/%m/%d/',blank=True, null=True,)
    doc_3 = models.ImageField(upload_to='belge_3/%Y/%m/%d/',blank=True, null=True,)
    doc_4 = models.ImageField(upload_to='belge_4/%Y/%m/%d/',blank=True, null=True,)
    doc_5 = models.ImageField(upload_to='belge_5/%Y/%m/%d/',blank=True, null=True,)
    doc_6 = models.ImageField(upload_to='belge_6/%Y/%m/%d/',blank=True, null=True,)
    doc_7 = models.ImageField(upload_to='belge_7/%Y/%m/%d/',blank=True, null=True,)
    doc_8 = models.ImageField(upload_to='belge_8/%Y/%m/%d/',blank=True, null=True,)
    def __str__(self):
       return str(self.user_restaurant)



class Delivery(models.Model):
    courier = models.ForeignKey('Courier', related_name='courier',  on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, related_name='restaurant', on_delete=models.PROTECT)
    confirm = models.BooleanField(default=False)
    count = models.PositiveIntegerField(default=0)
    active_count = models.PositiveIntegerField(default=0)
    sos = models.BooleanField(default=False)
    sos_reason = models.CharField(max_length=2, default="0")
    sos_result = models.CharField(max_length=2, default="0")
    self_delivery = models.BooleanField(default=False)    
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
       return str(self.restaurant)


@receiver(pre_save, sender=Delivery)
def delivery_create_update(sender, instance, **kwargs):
    courier = instance.courier
    print("delivery_create_update")
    print(courier.device_id)
    if not instance.self_delivery:
        try:
            status_old = sender.objects.get(pk=instance.pk)
            # send push notification fot updated delivery if courier changes
            if not (instance.courier == status_old.courier): 
                device, created = APNSDevice.objects.get_or_create(
                                            registration_id=courier.device_id,
                                            defaults={'user': courier.user_courier}
                                            )
                print("sender -teslimat - exists")
                msg={"title" : "Update", "body" : "Bob updates delivery details"}
                extra={"delivery_id": instance.id}
                print(msg)
                device.send_message(message=msg, sound="default", category="ID_CATEGORY_DELIVERY", extra=extra)

        except sender.DoesNotExist:
            # send push-notif for new delivery
            device, created = APNSDevice.objects.get_or_create(
                                        registration_id=courier.device_id,
                                        defaults={'user': courier.user_courier}
                                        )
            print("sender - teslimat - doesnot exist")
            msg={"title" : "New delivery", "body" : "Bob wants new delivery"}
            extra={"delivery_id": instance.id}
            print(msg)
            device.send_message(message=msg, sound="default", category="ID_CATEGORY_DELIVERY", extra=extra)





class Order(models.Model):
    delivery = models.ForeignKey(Delivery, related_name='order_delivery', on_delete=models.PROTECT)
    process_type = models.CharField(max_length=2, default="0")
    full_name = models.CharField(max_length=60, default="")
    tel_no = models.CharField(max_length=10, default="")
    address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
    longitude = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
    non_delivery_reason = models.CharField(max_length=2, default="0")
    non_payment_reason = models.CharField(max_length=2, default="0")
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.full_name


class Courier(models.Model):
    user_courier = models.OneToOneField(User, related_name="user_courier", on_delete=models.PROTECT, primary_key=True)
    state = models.CharField(max_length=2, default="0")
    active_restaurant = models.ForeignKey(Restaurant, related_name="active_restaurant", blank=True, null=True,  on_delete=models.CASCADE)
    active_delivery = models.ForeignKey(Delivery, related_name="active_delivery", blank=True, null=True,  on_delete=models.CASCADE)
    active_order = models.ForeignKey(Order, related_name="active_order",  blank=True, null=True, on_delete=models.CASCADE)
    queue = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=16, decimal_places=12, default="0.0")
    longitude = models.DecimalField(max_digits=16, decimal_places=12,  default="0.0")
    worker_active = models.BooleanField(default=True)
    tel_no = models.CharField(max_length=10, default="")
    pin = models.CharField(max_length=6, default="")
    registered_restaurants = models.ManyToManyField(Restaurant, blank=True)
    device_platform = models.CharField(max_length=1, choices=DEVICE_PLATFORM, default="0")
    device_id = models.CharField(max_length=100, default="0")

    def __str__(self):
        return str(self.user_courier.username)



@receiver(pre_save, sender=Courier)
def courier_queue_change(sender, instance, **kwargs):
    print("courier queue change")
    
    try:
        status_old = sender.objects.get(pk=instance.pk)
        # ws message if status changed from 3-serviste to 1-sırada
        if  (status_old.state == "3") and (instance.state == "1"): 
            queue_message = {"type": "state_change", 
                            "state": instance.state, 
                            "queue": instance.queue
                            }
            channel_layer = get_channel_layer()       
            channel_obj = WSClients.objects.filter(user=instance.user_courier).last()
            channel_name = channel_obj.channel_name
            print("3>>1")
            print(channel_layer)
            print(channel_name)
            async_to_sync(channel_layer.send)(channel_name, queue_message)
            print("message has been send")

        # ws message if status is 1-sırada  and queue changed
        if  (status_old.state == "1") and (instance.state == "1") and (status_old.queue != instance.queue): 
            queue_message = {"type": "queue_change", 
                             "state": instance.state, 
                             "queue": instance.queue
                            }
            channel_layer = get_channel_layer()   
            channel_obj = WSClients.objects.filter(user=instance.user_courier).last()
            channel_name = channel_obj.channel_name
            print("1>>1  queue change")
            print(channel_layer)
            print(channel_name)                
            async_to_sync(channel_layer.send)(channel_name, queue_message)                            
 

    except sender.DoesNotExist:
        print("sender - courier does not exist")




class WSClients(models.Model):
    user =  models.ForeignKey(User, related_name='wsclients', on_delete=models.PROTECT)
    channel_name = models.CharField(max_length=100, default="")
    def __str__(self):
        return '%s-%s' % (self.user, self.channel_name)






class Notification(models.Model):
    notif_type = models.CharField(max_length=2, default="0")
    receiver =  models.ForeignKey(User, related_name='receiver', on_delete=models.PROTECT)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.PROTECT)
    message = models.TextField(blank=True, null=True)
    viewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s-%s' % (self.sender, self.timestamp)



class Tip(models.Model):
    courier = models.ForeignKey(Courier, related_name='tip_courier', on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2,)
    def __str__(self):
       return self.tip_courier


class ExtraCourier(models.Model):
    courier = models.ForeignKey(Courier, related_name='extracourier_courier', on_delete=models.PROTECT)
    max_courier = models.PositiveIntegerField(default=0)
    amount_extra_courier = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)    
    def __str__(self):
       return self.courier


class InvoiceDetail(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='invoicedetail_restaurant', on_delete=models.PROTECT)
    year = models.PositiveIntegerField(default=0)
    month = models.PositiveIntegerField(default=0)
    max_courier = models.PositiveIntegerField(default=0)
    standard_addition = models.BooleanField(blank=True, null=True) 
    added_person = models.PositiveIntegerField(default=0)
    added_total = models.PositiveIntegerField(default=0) 
    standard_amount = models.PositiveIntegerField(default=0) 
    added_amount = models.PositiveIntegerField(default=0) 
    def __str__(self):
        return '%s-%s-%s' % (self.restaurant, self.year, self.month)


class InvoiceTotal(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='invoicetotal_restaurant', on_delete=models.PROTECT)
    year = models.PositiveIntegerField(default=0)
    month = models.PositiveIntegerField(default=0)
    paid = models.BooleanField(blank=True) 
    amount = models.PositiveIntegerField(default=0) 
    def __str__(self):
        return '%s-%s-%s' % (self.restaurant, self.year, self.month)



class StandardPrice(models.Model):
    max_courier = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    def __str__(self):
        return '%s-%s' % (self.max_courier, self.price)


class AddedPrice(models.Model):
    standard_price = models.ForeignKey(StandardPrice, related_name='addedprice_standardprice', on_delete=models.PROTECT)    
    extra_courier = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    def __str__(self):
        return '%s-%s-%s' % (self.standard_price, self.extra_courier, self.price)


class City(models.Model):
    name = models.CharField(max_length=80, default="İstanbul")
    def __str__(self):
        return '%s' % (self.name)

class Town(models.Model):
    city = models.ForeignKey(City, related_name='ilce_il', on_delete=models.PROTECT)    
    name = models.CharField(max_length=80, default="Kadıköy")
    def __str__(self):
        return '%s-%s' % (self.city, self.name)

class District(models.Model):
    Town = models.ForeignKey(Town, related_name='mahalle_ilce', on_delete=models.PROTECT)    
    name = models.CharField(max_length=80, default="Fenerbahçe")
    def __str__(self):
        return '%s-%s-%s' % (self.Town.City, self.Town, self.name)





