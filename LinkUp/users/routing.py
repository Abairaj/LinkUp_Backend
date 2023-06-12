from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path('userConnect/<user_id>', consumers.UserConsumer.as_asgi()),

]
