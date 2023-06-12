import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing
import users.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LinkUp.settings')
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(URLRouter(
        # chat.routing.websocket_urlpatterns,
        users.routing.websocket_urlpatterns
        
    ))
})
