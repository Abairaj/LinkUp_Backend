from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Notifications
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




class VideoChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'Video_call_{self.room_name}'
        print(self.room_name,'<<<<<<<<<<<<<<<<<<')

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        
    

    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        email = text_data_json['email']
        room_id = text_data_json['room_id']
        event = text_data_json['event']

        
        
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'send_message',
                'message':{'email':email,'room_id':room_id}
            }
        )
    
    async def disconnect(self, code):
        return await super().disconnect(code)
    

    async def send_message(self,event):
        message = event['message']

        print(message,'llllllllll')


        await self.send(text_data=json.dumps({
            'message':message
        }))






@database_sync_to_async
def create_notification(receiver,type="task_created",status="unread"):
    notification_to_create=Notifications.objects.create(receiver=receiver,type=type)
    print('I am here to help')
    return (notification_to_create.receiver.username,notification_to_create.type)



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'test_consumer'
        self.room_group_name = 'test_consumer_group'
        await  self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        await self.send(text_data=json.dumps({'status':"connected from django channels"}))
    

    async def receive(self, text_data=None):
        print(text_data)

        await self.send(text_data=json.dumps({'status':'we got you'}))


    

    async def disconnect(self, code):
        print('doconnected')
    
    async def send_notification(self,event):
        print(event)

    