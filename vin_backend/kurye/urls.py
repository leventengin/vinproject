from .views import UserViewSet, AnaFirmaViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.generic import TemplateView

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

urlpatterns = [
]

urlpatterns += router.urls
