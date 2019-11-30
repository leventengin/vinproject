from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import WSClient, Ticket
from channels.db import database_sync_to_async
from channels.auth import login
from django.contrib.auth import get_user_model


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

        """
        print(self.scope['user']) 
        if user.is_anonymous:
            print("anonymous")
            await self.close()
        else:
            print("not anonymous")
            await self.accept()
        """


    async def disconnect(self, close_code):
        print("-------------close---------")
        await self.close()


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        latitude = float(text_data_json['latitude'])
        longitude = float(text_data_json['longitude'])
        rid = text_data_json['rid']
        i = int(text_data_json['i'])    
        print(type)
        print(latitude)
        print(longitude)
        print(rid)
        print(i)




    @database_sync_to_async
    def _find_user(self, ticket):
        User=get_user_model()
        ticket_obj = Ticket.objects.filter(key=ticket).first()
        if ticket_obj:
            user_obj = ticket_obj.user
        else:
            user_obj = ""
        return user_obj







class RestoranConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']        
        print("----------connect  restoran-------------")
        print(self.scope['user']) 
        if user.is_anonymous:
            print("anonymous")
            await self.close()
        else:
            print("not anonymous")
            wsclient_create = await self._create_wsclient(event.get('data'))
            await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        print("-------------close  restoran ---------")
        await self.close()


    @database_sync_to_async
    def _create_wsclient(self, content):
        wsclient_obj = WSClient.objects.filter(user=self.user)
        if wsclient_obj:
            for wscli  in wsclient_obj:
                wscli.delete()
        WSClient.objects.create(user=self.user, channel_name=self.channel_name)
        return True

