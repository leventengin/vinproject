from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.serializers.json import DjangoJSONEncoder
from channels.db import database_sync_to_async
from channels.auth import login
from django.contrib.auth import get_user_model
from .restlist import calculate_distance, siraya_gir
from channels.layers import get_channel_layer
import requests
from .models import Restaurant, Courier, WSClients
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
            db_obj = await self._create_channel(user, self.channel_name)
            await self.accept()


    async def disconnect(self, close_code):
        print("-------------close---------")
        user = self.scope['user']
        db_obj = await self._delete_channel(user)        
        await self.close()



    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        user = self.scope['user']
        if type == "send_location":
            latitude = Decimal(text_data_json['latitude'])
            longitude = Decimal(text_data_json['longitude'])
            print(type)
            print(latitude)
            print(longitude)
            print(user)
            db_obj = await self._update_location(latitude, longitude, user.id)
        return None


    async def state_change(self, event):
        # Send a message down to the client
        state = event.get('state', None)
        queue = event.get('queue', None)
        print ("state & queue", state, "/", queue)
        print(event)
        await self.send(text_data=json.dumps(event))


    async def queue_change(self, event):
        # Send a message down to the client
        state = event.get('state', None)
        queue = event.get('queue', None)
        print ("state & queue", state, "/", queue)
        print(event)
        await self.send(text_data=json.dumps(event))




    @database_sync_to_async
    def _update_location(self, latitude, longitude, user_id):
        print("update_location")
        print(user_id)
        #user = request.user
        #print(user)
        User = get_user_model()
        user = User.objects.get(pk=user_id)
        kurye = Courier.objects.get(user_courier_id=user_id)
        print("kurye inside update location", kurye)
        print("kurye.state", kurye.state)

        if kurye.state == "1" or kurye.state == "0":
            print("kurye state 1 or 0  --- pass")
        
        elif kurye.state == "2" or kurye.state == "4" or kurye.state == "5":
            kurye.latitude = latitude
            kurye.longitude = longitude
            kurye.save()

        elif kurye.state == "3":
            restoran_obj = kurye.active_restaurant       
            distance = calculate_distance(latitude, longitude, restoran_obj.latitude, restoran_obj.longitude )
            print("distance")
            print(distance)
            if (distance < 100):
                kurye.state = "1"
                kurye.queue = siraya_gir(restoran_obj.pk)
            kurye.latitude = latitude
            kurye.longitude = longitude
            kurye.save()

        return None



    @database_sync_to_async
    def _create_channel(self, user, channel_name):
        print("create channel")
        print(user)
        WSClients.objects.filter(user=user).delete()
        WSClients.objects.create(user=user, channel_name=channel_name)
        return None


    @database_sync_to_async
    def _delete_channel(self, user):
        print("delete channel")
        print(user)
        WSClients.objects.filter(user=user).delete()
        return None













class RestoranConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("----------connect-------------")
        user = self.scope['user']
        print(user)
        if user.is_anonymous:
            print("restaurant anonymous")
            await self.close()
        else:
            print("restaurant not anonymous")
            db_obj = await self._create_rest_channel(user, self.channel_name)
            await self.accept()


    async def disconnect(self, close_code):
        print("-------------restaurant close---------")
        user = self.scope['user']
        db_obj = await self._delete_rest_channel(user)        
        await self.close()


    async def rest_change(self, event):
        # Send a message down to the 
        print("rest-change")
        print(event)
        await self.send(text_data=json.dumps(event))


    @database_sync_to_async
    def _create_rest_channel(self, user, channel_name):
        print("create restaurant channel")
        print(user)
        WSClients.objects.filter(user=user).delete()
        WSClients.objects.create(user=user, channel_name=channel_name)
        return None


    @database_sync_to_async
    def _delete_rest_channel(self, user):
        print("delete restaurant channel")
        print(user)
        WSClients.objects.filter(user=user).delete()
        return None











