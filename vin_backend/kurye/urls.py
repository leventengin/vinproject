from .views import UserViewSet, CompanyViewSet, RestaurantViewSet, DeliveryViewSet, OrderViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.generic import TemplateView
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
router.register(r'firma', CompanyViewSet, base_name='firma')
router.register(r'restoran', RestaurantViewSet, base_name='restoran')
router.register(r'teslimat', DeliveryViewSet, base_name='teslimat')
router.register(r'siparis', OrderViewSet, base_name='siparis')

urlpatterns = [
    url(r'courier_get_self_data', views.courier_get_self_data),
    #url(r'send_location', views.send_location),
    url(r'start_working', views.start_working),
    url(r'select_restaurant', views.select_restaurant),
    url(r'get_delivery', views.get_delivery),  
    url(r'update_device', views.update_device),      
    url(r'register_courier', views.register_courier),
    url(r'create_delivery', views.create_delivery),
    url(r'create_self_delivery', views.create_self_delivery),    
    url(r'update_delivery', views.update_delivery),
    url(r'delivery_approve_reject', views.delivery_approve_reject),  
    url(r'delivery_process', views.delivery_process),   
    url(r'enter_queue', views.enter_queue),                
    url(r'quit_queue', views.quit_queue),
    url(r'end_of_work', views.end_of_work),  
    url(r'sos', views.sos),
    url(r'sos_cancel', views.sos_cancel),                
    url(r'record_courier_check', views.record_courier_check),
    url(r'record_courier_accept', views.record_courier_accept),   
    url(r'^token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^refresh', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^pin_login', views.pin_login, name='pin_login'),



    #url(r'courier_list_details', views.get_courier_list),  

]

urlpatterns += router.urls
