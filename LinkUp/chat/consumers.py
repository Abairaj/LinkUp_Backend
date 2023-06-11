from channels.generic.websocket import AsyncWebsocketConsumer
import json


class Chatconsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print(self.room_name, '//////////////////')

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # send message to room group
        print(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': message
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_message(self, event):
        message = event['message']

        # send message to socket

        print(message,'in send')

        await self.send(text_data=json.dumps({
            'message': message
        }))
