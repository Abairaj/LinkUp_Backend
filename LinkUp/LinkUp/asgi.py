# import os

# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LinkUp.settings')

# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http":django_asgi_app,
# })


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing
from django.urls import path
from chat.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LinkUp.settings')
application = get_asgi_application()

ws_pattern=routing.urlpatterns
application = ProtocolTypeRouter({
  'websocket':(URLRouter(ws_pattern))
})
