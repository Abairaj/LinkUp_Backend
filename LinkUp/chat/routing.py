from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path('chat/<room_name>', consumers.Chatconsumer.as_asgi())
]
