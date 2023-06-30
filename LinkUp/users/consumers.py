from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import user
from chat.models import Notifications
from chat.models import Message
from asgiref.sync import sync_to_async


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        user_instance = await self.get_user(user_id)
        room_name = user_instance.email
        room_group_name = f'{user_instance.phone}{user_instance.id}'
        await self.channel_layer.group_add(room_group_name, self.channel_name)
        await self.accept()

    @database_sync_to_async
    def get_user(self, user_id):
        return user.objects.get(id=user_id)

    async def add_notification(self, data):
        # Await the coroutine to get the User instance
        sender = await self.get_user(data['from'])
        # Await the coroutine to get the User instance
        receiver = await self.get_user(data['to'])
        notification = data['content']
        type_ = data['type']

        await sync_to_async(Notifications.objects.create)(sender=sender, receiver=receiver, notification=notification, type=type_)
        print('notification created')

    async def add_chat(self, data):
        # Await the coroutine to get the User instance
        sender = await self.get_user(data['from'])
        # Await the coroutine to get the User instance
        recipient = await self.get_user(data['to'])
        content = data['content']

        await sync_to_async(Message.objects.create)(sender=sender, recipient=recipient, content=content)
        print('message created')

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            event = text_data_json.get('event')

            if event == 'notification':
                to = text_data_json.get('to')
                frm = text_data_json.get('from')
                content = text_data_json.get('content')
                type_ = text_data_json.get('type')
                data = {
                    'to': to,
                    'from': frm,
                    'content': content,
                    'type': type_
                }

                await self.add_notification(data)

                user_instance = await self.get_user(to)
                room_group_name = f'{user_instance.phone}{user_instance.id}'
                await self.channel_layer.group_send(
                    room_group_name,
                    {
                        'type': 'notification',
                        'message': {
                            'event': 'notification',
                            'content': content,
                            'from': frm,

                        }
                    }
                )

            if event == 'join:room':
                rec_user_id = text_data_json.get('rec_user_id')
                sender_user_id = text_data_json.get('sender_user_id')
                email = text_data_json.get('email')
                user_instance = await self.get_user(rec_user_id)
                room_group_name = f'{user_instance.phone}{user_instance.id}'
                await self.channel_layer.group_send(
                    room_group_name,
                    {
                        'type': 'join_room',
                        'message': {
                            'event': 'join_room',
                            'user_id': sender_user_id,
                            'rec_id': rec_user_id,
                            'email': email,
                        }
                    }
                )


            

            if event == 'call_user':
                to = text_data_json.get('to')
                frm = text_data_json.get('from')
                offer = text_data_json.get('offer')

                user_instance = await self.get_user(to)
                room_group_name = f'{user_instance.phone}{user_instance.id}'
                await self.channel_layer.group_send(
                    room_group_name,
                    {
                        'type': 'incoming_call',
                        'message': {
                            'event': 'incoming_call',
                            'offer': offer,
                            'from': frm,

                        }
                    }
                )

            if event == 'call_accepted':
                frm = text_data_json.get('from')
                to = text_data_json.get('to')
                answer = text_data_json.get('answer')

                user_instance = await self.get_user(to)
                room_group_name = f'{user_instance.phone}{user_instance.id}'
                await self.channel_layer.group_send(
                    room_group_name,
                    {
                        'type': 'call_accepted',
                        'message': {
                            'event': 'call_accepted',
                            'from': frm,
                            'answer': answer
                        }
                    }
                )

            if event == 'negotiationneeded':
                to = text_data_json.get('to')
                frm = text_data_json.get('from')
                offer = text_data_json.get('offer')

                user_instance = await self.get_user(to)
                room_group_name = f'{user_instance.phone}{user_instance.id}'
                await self.channel_layer.group_send(
                    room_group_name,
                    {
                        'type': 'negotiationneeded',
                        'message': {
                            'event': 'negotiationneeded',
                            'offer': offer,
                            'from': frm

                        }
                    }
                )

            if event == 'nego_done':
                answer = text_data_json.get('answer')
                to = text_data_json.get('to')

                user_instance = await self.get_user(to)
                room_group_name = f'{user_instance.phone}{user_instance.id}'
                await self.channel_layer.group_send(
                    room_group_name,
                    {
                        'type': 'nego_done',
                        'message': {
                            'event': 'nego_done',
                            'answer': answer,
                        }
                    }
                )

            if event == 'chat':
                message = text_data_json.get('message')
                to = text_data_json.get('to')
                frm = text_data_json.get('from')
                data = {'from': frm, 'to': to, 'content': message}
                await self.add_chat(data)
                print('chating......')
                user_instance = await self.get_user(to)
                room_group_name = f'{user_instance.phone}{user_instance.id}'
                await self.channel_layer.group_send(
                    room_group_name,
                    {
                        'type': 'chat',
                        'message': {
                            'event': 'chatmessage',
                            'content': message,
                        }
                    }
                )

    async def join_room(self, event):
        message = event.get('message')
        await self.send(text_data=json.dumps({'message': message}))

    async def incoming_call(self, event):
        message = event.get('message')
        await self.send(text_data=json.dumps({'message': message}))

    async def call_accepted(self, event):
        message = event.get('message')
        await self.send(text_data=json.dumps({'message': message}))

    async def negotiationneeded(self, event):
        message = event.get('message')
        await self.send(text_data=json.dumps({'message': message}))

    async def nego_done(self, event):
        message = event.get('message')
        await self.send(text_data=json.dumps({'message': message}))

    async def chat(self, event):
        message = event.get('message')
        await self.send(text_data=json.dumps({'message': message}))

    async def notification(self, event):
        message = event.get('message')
        await self.send(text_data=json.dumps({'message': message}))
