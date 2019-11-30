from .views import UserViewSet, AnaFirmaViewSet, FirmaViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.generic import TemplateView
#from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth import views
from . import views

"""
urlpatterns = [
    path('user/', views.UserViewSet, name='user'),
    path('grup/', views.AnaFirmaViewSet, name='grup'),
]

"""
router = DefaultRouter()
router.register(r'user', UserViewSet, base_name='user')
router.register(r'anafirma', AnaFirmaViewSet, base_name='anafirma')
router.register(r'firma', FirmaViewSet, base_name='firma')


urlpatterns = [
    url(r'courier_login', views.courier_login),
    url(r'send_location', views.send_location),
    url(r'register_courier', views.register_courier),
    url(r'record_courier_check', views.record_courier_check),
    url(r'record_courier_accept', views.record_courier_accept),
    #url(r'^auth-token', obtain_jwt_token),
    #url(r'^auth-token-refresh', refresh_jwt_token),
    #url(r'^auth-token-verify', verify_jwt_token),    
    url(r'^token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^refresh', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^pin', views.pin_login, name='pin_login'),



    #url(r'courier_list_details', views.get_courier_list),  

]

urlpatterns += router.urls
