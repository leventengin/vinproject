from channels.generic.websocket import AsyncWebsocketConsumer
import json

class KuryeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("----------connect-------------")
        print(self.scope['url_route']) 
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print("-------------close---------")
        await self.close()

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        print(type)

