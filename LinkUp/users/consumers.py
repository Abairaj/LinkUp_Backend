from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import user


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        user_instance = await self.get_user(user_id)
        room_name = user_instance.email
        room_group_name = f'{user_instance.phone}{user_instance.id}'
        print(user_id, 'pppppppppppppppppppp')
        await self.channel_layer.group_add(room_group_name, self.channel_name)
        print('accepted..............')
        await self.accept()

    @database_sync_to_async
    def get_user(self, user_id):
        return user.objects.get(id=user_id)

    async def receive(self, text_data=None, bytes_data=None):
        print('......................................')
        if text_data:
            text_data_json = json.loads(text_data)
            event = text_data_json.get('event')

            print(text_data, ';;;;;;;;;;;;')

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
                            'email': email,
                        }
                    }
                )

            if event == 'call_user':
                print('000000000000000000000000')
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
                            'from':frm,
                            
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
                            'from':frm

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
                            'answer':answer,
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

