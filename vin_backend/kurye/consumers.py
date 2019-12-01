from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import WSClient
from channels.db import database_sync_to_async
from channels.auth import login
from django.contrib.auth import get_user_model
from .restlist import calculate_distance, siraya_gir


class KuryeConsumer(AsyncWebsocketConsumer):
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

        if type == "send_location":
            latitude = float(text_data_json['latitude'])
            longitude = float(text_data_json['longitude'])
            user_id = int(text_data_json['user_id'])
            print(type)
            print(latitude)
            print(longitude)
            print(user_id)
            db_obj = _update_location(user_id, latitude, longitude)
            data = {"type": "location_response",
                    "courier_status": db_obj.courier_status,
                    "queue_order": db_obj.queue_order,
            }
            await channel_layer.send("channel_name", data)


        if type == "get_queue_order":
            user_id = int(text_data_json['user_id'])
            print(type)
            print(user_id)
            db_obj = _get_order(user_id)
            data = {"type": "queue_order_response",
                    "courier_status": db_obj.courier_status,
                    "queue_order": db_obj.queue_order,
            }
            await channel_layer.send("channel_name", data)



    @database_sync_to_async
    def _update_location(self, user_id, latitude, longitude):
        User=get_user_model()
        user_obj = User.objects.filter(id=user_id).first()
        bagli_restoran = user_obj.aktif_firma
        restoran_obj = Firma.objects.filter(id=bagli_restoran).first()       
        distance = calculate_distance(latitude, longitude, rest_obj.enlem, rest_obj.boylam )
        print("-------")
        print(distance)
        if (distance < 20) & (user_obj.durum == "1"):
            user_obj.durum = "3"
            sira = siraya_gir(restoran_obj.id)
        user_obj.enlem = latitude
        user_obj.boylam = longitude
        user_obj.save()
        db_obj = {"courier_status": user_obj.durum, "queue_order": user_obj.sira}
        return db_obj


    @database_sync_to_async
    def _get_order(self, user_id):
        User=get_user_model()
        user_obj = User.objects.filter(id=user_id).first()
        db_obj = {"courier_status": user_obj.durum, "queue_order": user_obj.sira}
        return db_obj













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



