from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import user

class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        usr = await self.get_user(user_id)
        room_name = usr.email
        room_group_name = f'{usr.username}@{usr.email}'
        await self.accept()

    @database_sync_to_async
    def get_user(self,user_id):
        return user.objects.get(id = user_id)
    
    async def receive(self, text_data=None):
        print(text_data)
        text_data_json = json.loads(text_data)
        event = text_data_json['event']

        if event == 'call_user':
            user_id = text_data_json['user_id']
            room_id = text_data_json['room_id']

            usr =  await self.get_user(user_id)
            room_group_name = f'{usr.username}@{usr.email}'
            await self.channel_layer.group_send(

                room_group_name,
                {
                    'type':'incoming_call',
                    'message':{
                        'room_id':room_id,
                        'username':usr.username
                    }
                }

            )