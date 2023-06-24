import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter,get_default_application
from channels.auth import AuthMiddlewareStack
import users.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LinkUp.settings')
django_asgi_app = get_default_application()
# get_asgi_application()


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(URLRouter(
        users.routing.websocket_urlpatterns
        
    ))
})
