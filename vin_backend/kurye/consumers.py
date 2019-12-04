from channels.generic.websocket import AsyncWebsocketConsumer
import json
#from .models import WSClient
from channels.db import database_sync_to_async
from channels.auth import login
from django.contrib.auth import get_user_model
from .restlist import calculate_distance, siraya_gir
from channels.layers import get_channel_layer
import requests
from .models import Firma
from decimal import Decimal


class KuryeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("----------connect-------------")
        user = self.scope['user']
        print(user)
        if user.is_anonymous:
            print("anonymous")
            await self.close()
        else:
            print("not anonymous")
            await self.accept()


    async def disconnect(self, close_code):
        print("-------------close---------")
        await self.close()


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        #channel_layer = get_channel_layer()
        #channel_name = self.channel_name
        user = self.scope['user']
        if type == "send_location":
            latitude = Decimal(text_data_json['latitude'])
            longitude = Decimal(text_data_json['longitude'])
            print(type)
            print(latitude)
            print(longitude)
            print(user)
            #self._update_location(latitude, longitude, user,id)
            db_obj = await self._update_location(latitude, longitude, user.id)
            #print("updated location")
            #print(db_obj)
        return None



    async def location_response(self, order_obj):
        #order_obj = _get_order()
        await self.send(order_obj)
        return None


    @database_sync_to_async
    def _update_location(self, latitude, longitude, user_id):
        print("update_location")
        print(user_id)
        #user = request.user
        #print(user)
        User = get_user_model()
        user = User.objects.get(id=user_id)
        print("user inside update location", user)
        if user.durum == "1":
            bagli_restoran_id = user.aktif_firma
            restoran_obj = Firma.objects.filter(pk=bagli_restoran_id).first()       
            distance = calculate_distance(latitude, longitude, restoran_obj.enlem, restoran_obj.boylam )
            print("-------")
            print(distance)
            if (distance < 20):
                user.durum = "3"
                user.sira = siraya_gir(restoran_obj.id)
        user.enlem = latitude
        user.boylam = longitude
        user.save()
        #db_obj = {"courier_status": user.durum, "queue_order": user.sira}
        return None



    @database_sync_to_async
    def _get_order(self):
        user = request.user
        print("_get_order", user.durum, "-", user.sira)
        order_obj = {"type": "location_response", 
                     "courier_status": user.durum, 
                     "queue_order": user.sira
                     }
        return order_obj













class RestoranConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #user = self.scope['user']
        print("----------connect-------------")
        user = self.scope['user']
        print(user)
        if user.is_anonymous:
            print("anonymous")
            await self.close()
        else:
            print("not anonymous")
            await self.accept()


    async def disconnect(self, close_code):
        print("-------------close---------")
        await self.close()


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        channel_name = self.channel_name

        if type == "get_couriers":
            firma_id = int(text_data_json['firma_id'])
            print(type)
            print(firma_id)
            db_obj = _get_courier_list(firma_id)
            data = {"type": "response_get_couriers",
                    "courier_list": db_obj,
            }
            await channel_layer.send("channel_name", data)




    @database_sync_to_async
    def _get_courier_list(self, firma_id):
        User=get_user_model()
        db_obj = {}
        firma_obj = Firma.objects.filter(id=firma_id).first()
        couriers = firma_obj.kayitli_motorcular
        for i in couriers:
            courier_obj = User.objects.filter(id=i).first()
            if courier_obj:
                courier_data = {"id": courier_obj.id,
                                "name": courier_obj.first_name,
                                "surname": courier_obj.last_name,
                                "state": courier_obj.durum,
                                "latitude": courier_obj.enlem,
                                "longitude": courier_obj.boylam,
                                "order": courier_obj.sira,
                                }
                db_obj[courier_obj.id] = courier_data
        
        return db_obj



