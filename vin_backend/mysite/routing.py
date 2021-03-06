from django.urls import path 
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack  
from channels.routing import ProtocolTypeRouter, URLRouter  
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from kurye.consumers import KuryeConsumer, RestoranConsumer
from .channelsmiddleware import TokenAuthMiddleware



application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        AuthMiddlewareStack (
             URLRouter([
                     url(r'^kurye/$', KuryeConsumer),
                     url(r'^restoran/$', RestoranConsumer),                    
             ])
        ))
})



