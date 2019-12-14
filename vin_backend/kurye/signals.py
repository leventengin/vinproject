from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField, JSONField
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .consumers import location_response 
from django.contrib.auth import get_user_model
from .models import Teslimat
from push_notifications.models import APNSDevice, GCMDevice




@receiver(pre_save, sender=get_user_model())
def status_change(sender, instance, **kwargs):
    try:
        status_old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass 
    else:
        if (instance.durum == "3") & ((status_old.durum != instance.durum) | (status_old.sira != instance.sira)) : 
            order_obj = {"type": "location_response", 
                        "courier_status": user.durum, 
                        "queue_order": user.sira
                        }
            async_to_sync(location_response(order_obj))





