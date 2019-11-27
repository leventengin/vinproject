from django.urls import path 
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack  
from channels.routing import ProtocolTypeRouter, URLRouter  
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from kurye.consumers import KuryeConsumer

# changed
application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(

             URLRouter([
                     path('kurye', KuryeConsumer),
                     #url(r"^kurye/$", KuryeConsumer),
             ])
        )
})



#url(r"^front(end)/$", consumers.AsyncChatConsumer)