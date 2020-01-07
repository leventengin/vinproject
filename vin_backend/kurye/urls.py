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
from .views import ProfilePictureUploadView, PicProfileUploadView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


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
    url(r'^courier_get_self_data/$', views.courier_get_self_data),
    url(r'^start_working/$', views.start_working),
    url(r'^select_restaurant/$', views.select_restaurant),
    url(r'^get_delivery/$', views.get_delivery),  
    url(r'^update_device/$', views.update_device),      
    url(r'^create_delivery/$', views.create_delivery),
    url(r'^create_self_delivery/$', views.create_self_delivery),    
    url(r'^update_delivery/$', views.update_delivery),
    url(r'^delivery_approve_reject/$', views.delivery_approve_reject),  
    url(r'^delivery_process/$', views.delivery_process),   
    url(r'^enter_queue/$', views.enter_queue),                
    url(r'^quit_queue/$', views.quit_queue),
    url(r'^end_of_work/$', views.end_of_work),  
    url(r'^sos/$', views.sos),
    url(r'^sos_cancel/$', views.sos_cancel),  
    url(r'^pic_profile/$', PicProfileUploadView.as_view()),                
    url(r'^record_courier_check/$', views.record_courier_check),
    url(r'^record_courier_accept/$', views.record_courier_accept),   
    url(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #url(r'^token/$', obtain_jwt_token, name='token_obtain_pair'),
    url(r'^refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    #url(r'^refresh/$', refresh_jwt_token, name='token_refresh'),    
    url(r'^pin_login/$', views.pin_login, name='pin_login'),
    url(r'^login/$', views.login, name='login'),    
    url(r'^forget_pw/$', views.forget_pw, name='forget_pw'),    
    url(r'^create_new_pw/$', views.create_new_pw, name='create_new_pw'),    
    url(r'^rest_get_data/$', views.rest_get_data, name='rest_get_data'),
    url(r'^get_access_token/$', views.get_access_token, name='get_access_token'),
    url(r'^list_district/$', views.list_district, name='list_district'),
    url(r'^create_courier/$', views.create_courier, name='create_courier'),
    #url(r'^register_courier/$', views.register_courier, name='register_courier'),
    #url(r'^unregister_courier/$', views.unregister_courier, name='unregister_courier'),
    #url(r'^create_pin/$', views.create_pin, name='create_pin'),
]

urlpatterns += router.urls
