from django.urls import path 
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack  
from channels.routing import ProtocolTypeRouter, URLRouter  
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from kurye.consumers import KuryeConsumer, RestoranConsumer


application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack (
             URLRouter([
                     url(r'^kurye/(?P<ticket>\w+)/$', KuryeConsumer),
                     url(r'^restoran/$', RestoranConsumer),                    
             ])
        ))
})


