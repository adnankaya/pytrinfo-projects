"""
ASGI config for src project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter # yeni
from channels.auth import AuthMiddlewareStack # yeni
from channels.security.websocket import AllowedHostsOriginValidator # yeni
# yeni
from myapp.routing import websocket_urlpatterns as myapp_websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # websocket konfigurasyonlari yazilacak...
     "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(myapp_websocket_urlpatterns))
        ),
})
