from django.urls import path
from . import consumers

urlpatterns = [
    path('chat/', consumers.ChatConsumer.as_asgi()),
]
