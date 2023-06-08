from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.group_name = f'room_{self.room_name}'


        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

        data = {"type":"connected"}

        self.send(text_data=json.dumps({
            "payload":"connected"
        }))

    def disconnect(self,close_code):
        # close connection
        pass
#chenged....................................................................
    def receive(self,text_data):
        # incoming messages
        pass

    # def send_message(self,close_code):
    #     # send messages
    #     pass
