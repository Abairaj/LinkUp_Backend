from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path('chat/<room_name>', consumers.Chatconsumer.as_asgi()),
    path('video_call/<room_name>', consumers.VideoChatConsumer.as_asgi())

]
