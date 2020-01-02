
from rest_framework import viewsets
from django.conf import settings
from .models import User, Company, Restaurant, Delivery, Order, Courier
from .serializers import UserSerializer, CompanySerializer, RestaurantSerializer, CourierSerializer
from .serializers import DeliverySerializer, OrderSerializer, ProfilePictureSerializer
from .serializers import RestSerializer
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
#from rest_framework import filters
from rest_framework import generics
from .pagination import StandardResultsSetPagination
from django_filters import rest_framework as filters
from django.utils.decorators import method_decorator
from mysite.settings import *
from django.core.validators import validate_email
from django.core.mail import EmailMessage
from .token import account_activation_token
from django import template
from django.template.loader import get_template
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os
from .models import User
import random
import string
from django.contrib.auth.models import User
from django.http import JsonResponse
import requests
from django.urls import reverse
import json 
from .restlist import siraya_gir, siradan_cik, get_rest_list, calculate_distance
from django_user_agents.utils import get_user_agent
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework import status
from django.core.files.images import ImageFile







def _pw(length=10):
    s = ''
    for i in range(length):
        s += random.choice(string.ascii_letters + string.digits)
    return s



class ProfilePictureUploadView(APIView):
    parser_class = (FileUploadParser,)
    def post(self, request, *args, **kwargs):
        file_serializer = ProfilePictureSerializer(data=request.data)
        if  file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    User = get_user_model()
    queryset = User.objects.all()

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

class DeliveryViewSet(viewsets.ModelViewSet):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()



@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def pin_login(request):
    print("-------------pin login---------------")
    pin = request.data.get("pin").rstrip()
    

    print(pin)
    if not pin:
        return Response({'success': False,
                         'message': 'Pin girilmemiş',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)
    
    User=get_user_model()

    try:
        kurye = Courier.objects.get(pin=pin)
    except:
        return Response({'success': False,
                         'message': 'Hatalı PIN!. Kayıtlı olduğunuz restorandan PIN inizi değiştirebilirsiniz.',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    if kurye.user_courier.is_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Hesap kapalı',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)
    
    new_password = _pw()
    #print("new password", new_password)
    kurye.user_courier.set_password(new_password)
    kurye.user_courier.save()

    print(kurye.user_courier.username, '/', kurye.user_courier.password)
    #json_data = JsonResponse({'username':user.username, 'password': user.password})
    json_data = {'username':kurye.user_courier.username, 'password': new_password}
    print(json_data)

    response_login = requests.post(
        request.build_absolute_uri(reverse('token_obtain_pair')),
        data=json_data
    )

    response_login_dict = json.loads(response_login.content)
    return Response(response_login_dict, response_login.status_code)





@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def rest_login(request):
    print("-------------restorant login---------------")
    username = request.data.get("username").rstrip()
    password = request.data.get("password")
    print(username)
    print(password)
    if not username or not password:
        return Response({'success': False,
                         'message': 'Lütfen kullanıcı adı ve parola giriniz',
                         'response' : None
                        },
                        status=HTTP_400_BAD_REQUEST)
    
    if '@' in username:
        pass
    else:
        return Response({'success': False,
                         'message': 'Lütfen eposta hesabı giriniz',
                         'response' : None
                        },
                        status=HTTP_400_BAD_REQUEST)

    User=get_user_model()
    try:
        user = User.objects.get(username=username)
    except:
        return Response({'success': False,
                         'message': 'Kullanıcı adı hatalı',
                         'response' : None
                        },
                        status=HTTP_400_BAD_REQUEST)

    check_password = user.check_password(password)
    if not check_password:
        return Response({'success': False,
                         'message': 'Parola hatalı',
                         'response' : None
                        },
                        status=HTTP_400_BAD_REQUEST)

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Hesap aktif değil',
                         'response' : None
                        },
                        status=HTTP_400_BAD_REQUEST)


    restaurant = Restaurant.objects.filter(user_restaurant=user).first()

    if not restaurant:
        return Response({'success': False,
                         'message': 'Restoran tanımlı değil',
                         'response' : None
                        },
                        status=HTTP_400_BAD_REQUEST)        


    json_data = {'username':username, 'password': password}
    print(json_data)

    response_login = requests.post(
        request.build_absolute_uri(reverse('token_obtain_pair')),
        data=json_data
    )

    response_login_dict = json.loads(response_login.content)
    return Response(response_login_dict, response_login.status_code)





@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def get_access_token(request):
    print("-------------get access token---------------")
    r_token = request.data.get("abc").rstrip()
    print(r_token)
    if not r_token:
        return Response({'success': False,
                         'message': 'Bilgi eksik',
                         'response' : None
                        },
                        status=HTTP_400_BAD_REQUEST)

    json_data = {'refresh':r_token}
    print(json_data)

    response_access = requests.post(
        request.build_absolute_uri(reverse('token_refresh')),
        data=json_data
    )
    print("response_access:", response_access.status_code)
    print("response_access_content:", response_access.content)

    response_access_dict = json.loads(response_access.content)
    print("response_access_dictionary_access:", response_access_dict["access"])    
    return Response(response_access_dict, response_access.status_code)








@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def rest_get_data(request):
    print("-------------restorant get data ---------------")
    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Hesap aktif değil',
                         'response' : None
                        },
                        status=HTTP_400_BAD_REQUEST)


    restaurant = Restaurant.objects.filter(user_restaurant=user).first()

    if not restaurant:
        return Response({'success': False,
                         'message': 'Restoran tanımlı değil',
                         'response' : None
                        },
                        status=HTTP_400_BAD_REQUEST)        


    serializer = RestSerializer(restaurant)

    return Response({'success': True,
                    'message': 'Başarılı oturum açış',
                    'response': {'restaurant': serializer.data }               
                    },
                    status=HTTP_200_OK)








@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def courier_get_self_data(request):
    print("-------------login_courier---------------")

    user = request.user
    #User=get_user_model() 
    #user = User.objects.get()
    print(user, user.id)

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    kurye = Courier.objects.get(user_courier=user)
    print(kurye)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

  
    serializer = CourierSerializer(kurye)

    return Response({'success': True,
                    'message': 'Başarılı',
                    'response': {'courier': serializer.data }               
                    },
                    status=HTTP_200_OK)






class PicProfileUploadView(APIView):
    parser_class = (FileUploadParser,)
    def post(self, request, format=None):
        if 'file' not in request.data:
            return Response({'success': False,
                        'message': 'Dosya yüklü değil',
                        'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

        f = request.data['file']
        print(f.name)
        user = request.user
        if user.is_active is False:
            return Response({'success': False,
                            'message': 'Kullanıcı aktif değil',
                            'response' : None,
                            },
                            status=HTTP_400_BAD_REQUEST)

        kurye = Courier.objects.get(user_courier=user)

        print(request.get_host())

        if kurye.worker_active is False:
            return Response({'success': False,
                            'message': 'Kullanıcı aktif değil',
                            'response' : None,
                            },
                            status=HTTP_400_BAD_REQUEST)

        user.pic_profile.save(f.name, f, save=True)
        print(user.pic_profile.url)
        full_path = request.get_host()+user.pic_profile.url
        print(full_path)

        user.pic_profile_abs_url = request.build_absolute_uri(user.pic_profile.url)
        user.save()

        kurye = Courier.objects.get(user_courier=user)
        serializer = CourierSerializer(kurye)
        return Response({'success': True,
                        'message': 'Başarılı yükleme',
                        'response': {'courier': serializer.data }                 
                        },
                        status=HTTP_200_OK)





@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def start_working(request):
    print("-------------start working---------------")
    latitude = request.data.get("latitude")
    longitude = request.data.get("longitude")
    print(latitude)
    print(longitude)
    if not latitude or not longitude:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    print(kurye)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    # en yakındaki restoranları listele, yoksa boş dön
    # kayıtlı değilse kayıtlı değil bilgisi dönüyor
    # not: şu an için hepsini dönüyor, test döneminde bu şekilde 
    
    rest_list = get_rest_list(latitude=latitude, longitude=longitude, user_id=user.id)

    return Response({'success': True,
                     'message': 'Başarılı',
                     'response' : {
                        'restaurant_list': rest_list
                     }},
                    status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def select_restaurant(request):
    print("---------select restaurant---------------")
    rest_id = request.data.get("rest_id")
    print(rest_id)
    if not rest_id:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    print(kurye)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    rest_obj = Restaurant.objects.filter(user_restaurant_id=rest_id).first()

    yeni_sira = siraya_gir(rest_obj.user_restaurant.id)
    
    kurye.queue = yeni_sira
    kurye.active_restaurant = rest_obj
    kurye.state = "1"
    kurye.save()


    serializer = CourierSerializer(kurye)

    return Response({'success': True,
                    'message': 'Restoran seçildi',
                    'response': {'courier': serializer.data }                
                    },
                    status=HTTP_200_OK)





@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def get_delivery(request):
    print("---------get delivery--------------")
    delivery_id = request.data.get("delivery_id")
    print(delivery_id)
    if not delivery_id:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    print(kurye)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)



    delivery_obj = Delivery.objects.filter(pk=delivery_id).first()
    serializer = DeliverySerializer(delivery_obj)

    return Response({'success': True,
                    'message': 'Başarıyla kaydedildi',
                    'response': { 'delivery': serializer.data }               
                    },
                    status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def update_device(request):
    print("---------update device--------------")
    device_platform = request.data.get("device_platform")
    device_id = request.data.get("device_id")
    print(device_platform)
    print(device_id)

    if not device_id  or  not device_platform:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    print(kurye)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)



    kurye.device_platform = device_platform
    kurye.device_id = device_id
    kurye.save()
  
    serializer = CourierSerializer(kurye)

    return Response({'success': True,
                    'message': 'Başarıyla kaydedildi',
                    'response': None,              
                    },
                    status=HTTP_200_OK)



    



@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def register_courier(request):
    print("-------------register_courier---------------")
    token = request.data.get("token")
    name = request.data.get("name")
    family_name = request.data.get("family_name")
    kendi_motoru = request.data.get("kendi_motoru")
    fulltime_parttime = request.data.get("fulltime_parttime")
    il = request.data.get("il")
    ilce = request.data.get("ilce")
    mahalle = request.data.get("mahalle")
    adress = request.data.get("adress")
    tel_no = request.data.get("tel_no")
    picture = request.FILES.get("picture")

    print(token)
    print(name)
    print(family_name)
    print(kendi_motoru)
    print(fulltime_parttime)
    print(il)
    print(ilce)
    print(mahalle)
    print(adress)
    print(tel_no)
    print(picture)


    # gelen yeni motorcu bilgilerinde token, ad , soyad eksik mi bak
    #---------------------------------------------------------------
    if not token or not name or not family_name:
        return Response({'success': 'false',
                        'message': 'Eksik bilgi gönderildi',
                        },
                        status=HTTP_400_BAD_REQUEST)

    # telefon numarası eksik mi bak, önemli
    if not tel_no:
            return Response({'success': 'false',
                            'message': 'Telefon numarası eksik',
                            },
                            status=HTTP_400_BAD_REQUEST)

    # gönderimi yapan restorant için token var mu bak,
    # token değişmiş olabilir bu durumda tekrar login olmalı
    try:
        token_obj = Token.objects.get(key=token)
    except:
        return Response({'success': 'false',
                        'message': 'Token bulunamadı, lütfen login olun',
                        },
                        status=HTTP_400_BAD_REQUEST)

    # aynı telefon numarası var mı  kontrol et, telefon numarası tek olmalı
    User = get_user_model()
    user_obj = User.objects.filter(tel_no=tel_no)
    if user_obj:
         return Response({'success': 'false',
                        'message': 'Bu kişi daha önce telefon numarası ile kayıtlı',
                        },
                        status=HTTP_400_BAD_REQUEST)

    # burada bilgileri gelmiş olan yeni motorcuyu kaydet
    # --------------------------------------------------

    password = _pw()
    print(password)

    User.objects.create(username=tel_no,
                        first_name=name,
                        last_name=family_name,
                        password=password,
                        tipi=0,
                        durum=0,
                        tel_no=tel_no,
                        #pic_profile=picture,
                        )

    user_obj = User.objects.last()
    print(user_obj.username)

    return Response({'success': 'true',
                    'message': 'Başarılı',
                    },
                    status=HTTP_200_OK)





@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def record_courier_check(request):
    print("-------------register_courier---------------")
    token = request.data.get("token")
    tel_no = request.data.get("tel_no")

    print(token)
    print(tel_no)

    # gelen yeni motorcu bilgilerinde token, ad , soyad eksik mi bak
    #---------------------------------------------------------------
    if not token:
        return Response({'success': 'false',
                        'message': 'Eksik bilgi gönderildi',
                        },
                        status=HTTP_400_BAD_REQUEST)

    # telefon numarası eksik mi bak, önemli
    if not tel_no:
            return Response({'success': 'false',
                            'message': 'Telefon numarası eksik',
                            },
                            status=HTTP_400_BAD_REQUEST)

    # gönderimi yapan restorant için token var mu bak,
    # token değişmiş olabilir bu durumda tekrar login olmalı
    try:
        token_obj = Token.objects.get(key=token)
    except:
        return Response({'success': 'false',
                        'message': 'Token bulunamadı, lütfen login olun',
                        },
                        status=HTTP_400_BAD_REQUEST)



    # burada bilgileri gelmiş olan yeni motorcuyu kontrol et uygun mu
    # ---------------------------------------------------------------

    user_obj = User.objects.filter(tel_no=tel_no).first()

    if user_obj.count() != 1:
        return Response({'success': 'false',
                        'message': 'Telefon numarası birden çok kayıtlı',
                        },
                        status=HTTP_400_BAD_REQUEST)

    token_obj = Token.objects.get(key=token)
    firma_obj = Restaurant.objects.filter(id=token_obj.user).first()

    if not(firma_obj):
        return Response({'success': 'false',
                        'message': 'Restorant kayıtlı değil',
                        },
                        status=HTTP_400_BAD_REQUEST)



    return Response({'success': 'true',    
                    'message': 'Başarılı login',
                    'courier': {'user_id': user_obj.id,
                                'pic_profile': user_obj.pic_profile,
                                'first_name': user_obj.first_name,
                                'last_name': user_obj.last_name,
                                'durum': user_obj.durum,
                                'tel_no': user_obj.tel_no,
                                'kayıtlı_motorcular': firma_obj.kayıtlı_motorcular,
                                }},
                    status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def record_courier_accept(request):
    print("-------------register_courier---------------")
    token = request.data.get("token")
    tel_no = request.data.get("tel_no")
    courier_list = request.data.get("courier_list")

    print(token)
    print(tel_no)
    print(courier_list)

    # gelen yeni motorcu bilgilerinde token, ad , soyad eksik mi bak
    #---------------------------------------------------------------
    if not token:
        return Response({'success': 'false',
                        'message': 'Eksik bilgi gönderildi',
                        },
                        status=HTTP_400_BAD_REQUEST)

    # telefon numarası eksik mi bak, önemli
    if not tel_no:
            return Response({'success': 'false',
                            'message': 'Telefon numarası eksik',
                            },
                            status=HTTP_400_BAD_REQUEST)

    # gönderimi yapan restorant için token var mu bak,
    # token değişmiş olabilir bu durumda tekrar login olmalı
    try:
        token_obj = Token.objects.get(key=token)
    except:
        return Response({'success': 'false',
                        'message': 'Token bulunamadı, lütfen login olun',
                        },
                        status=HTTP_400_BAD_REQUEST)


    # burada bilgileri gelmiş olan yeni motorcuyu kontrol et uygun mu
    # ---------------------------------------------------------------


    token_obj = Token.objects.get(key=token)
    firma_obj = Restaurant.objects.filter(id=token_obj.user).first()

    if not(firma_obj):
        return Response({'success': 'false',
                        'message': 'Restorant kayıtlı değil',
                        },
                        status=HTTP_400_BAD_REQUEST)

    firma_obj.kayitli_motorcular =  courier_list
    firma_obj.save()

    return Response({'success': 'true',
                    'message': 'Motorcu  kayıtlı listesine alındı',
                    },
                    status=HTTP_200_OK)





@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def courier_list_details(request):
    print("-------------courier list details ---------------")
    token = request.data.get("token")
    name = request.data.get("name")
    family_name = request.data.get("family_name")
    kendi_motoru = request.data.get("kendi_motoru")
    fulltime_parttime = request.data.get("fulltime_parttime")
    il = request.data.get("il")
    ilce = request.data.get("ilce")
    mahalle = request.data.get("mahalle")
    adress = request.data.get("adress")
    tel_no = request.data.get("tel_no")
    picture = request.FILES.get("picture")

    print(token)
    print(name)
    print(family_name)
    print(kendi_motoru)
    print(fulltime_parttime)
    print(il)
    print(ilce)
    print(mahalle)
    print(adress)
    print(tel_no)
    print(picture)


    # gelen yeni motorcu bilgilerinde token, ad , soyad eksik mi bak
    #---------------------------------------------------------------
    if not token or not name or not family_name:
        return Response({'success': 'false',
                        'message': 'Eksik bilgi gönderildi',
                        },
                        status=HTTP_400_BAD_REQUEST)

    # telefon numarası eksik mi bak, önemli
    if not tel_no:
            return Response({'success': 'false',
                            'message': 'Telefon numarası eksik',
                            },
                            status=HTTP_400_BAD_REQUEST)

    # gönderimi yapan restorant için token var mu bak,
    # token değişmiş olabilir bu durumda tekrar login olmalı
    try:
        token_obj = Token.objects.get(key=token)
    except:
        return Response({'success': 'false',
                        'message': 'Token bulunamadı, lütfen login olun',
                        },
                        status=HTTP_400_BAD_REQUEST)

    # aynı telefon numarası var mı  kontrol et, telefon numarası tek olmalı
    User = get_user_model()
    user_obj = User.objects.filter(tel_no=tel_no)
    if user_obj:
         return Response({'success': 'false',
                        'message': 'Bu kişi daha önce telefon numarası ile kayıtlı',
                        },
                        status=HTTP_400_BAD_REQUEST)

    # burada bilgileri gelmiş olan yeni motorcuyu kaydet
    # --------------------------------------------------

    password = _pw()
    print(password)

    User.objects.create(username=tel_no,
                        first_name=name,
                        last_name=family_name,
                        password=password,
                        tipi=0,
                        durum=0,
                        tel_no=tel_no,
                        #pic_profile=picture,
                        )

    user_obj = User.objects.last()
    prit(user_obj.username)

    return Response({'success': 'true',
                    'message': 'Başarılı',
                    },
                    status=HTTP_200_OK)










@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def rest_register(request):
    data = request.data
    username = data.get('username').rstrip()
    email = data.get('email').rstrip()
    password1 = data.get('password1')
    password2 = data.get('password2')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username_exist = User.objects.filter(username=username).exists()
    email_exist = User.objects.filter(email=email).exists()
    error = {}
    if username_exist:
        error['username'] = 'A user with that username already exists.'
    if email_exist:
        error['email'] = 'A user is already registered with this e-mail address.'
    if len(password1) < 8:
        error['password1'] = 'This password is too short. It must contain at least 8 characters.'
    if password1 != password2:
        error['non_field_error'] = 'The two password fields didn\'t match.'

    try:
        validate_email(email)
    except:
        error['email'] = 'Enter a valid email address.'

    if len(error) is not 0:
        return Response(error, status=HTTP_400_BAD_REQUEST)
    else:
        user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name, is_active=False)
        user.set_password(password1)
        user.save()
        token = Token.objects.create(user=user)
        mail_subject = 'Activate your blog account.'
        link = REACT_URL + '/token/' + str(user.id) + '/' + account_activation_token.make_token(user)
        ctx = { 'name': user.get_full_name(), 'link': link}
        message = get_template('registration_template.html').render(ctx)
        email = EmailMessage(
                mail_subject, message, to=[email], from_email=settings.EMAIL_HOST_USER
        )
        email.content_subtype = 'html'
        email.send()
        return Response({'status': "Activation mail send."}, status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def rest_activate(request):
    try:
        activate_token = request.data.get('token')
        uid = request.data.get('uid')
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, activate_token):
        user.is_active = True
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'roles': user.profile.user_role.values_list('name'), 'email': user.email}, status=HTTP_200_OK)
    else:
        return Response("error", status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def create_delivery(request):
    print("-------------create delivery---------------")
    address_list = request.data.get("address_list")
    count = request.data.get("count")
    courier_id = request.data.get("courier_id")
    restaurant_id = request.data.get("restaurant_id")
    print(address_list)
    print(count)
    print(courier_id)
    print(restaurant_id)
    if not address_list or not count  or not courier_id or not restaurant_id:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    print(kurye)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    # not: restorandan gelen bilgilere göre yeni bir teslimat ve ilişkili işlemler yarat 
    print("teslimat yaratma öncesi")
    delivery_obj = Delivery.objects.create( 
                                        courier_id=courier_id,
                                        restaurant_id=restaurant_id,
                                        count=count,
                                        active_count=count
                                        )
   
    print( "islem teslimat yaratma öncesi")
    print(address_list[0])
    print(address_list[1])
    i = 0
    x = len(address_list)
    print("len", x)
    while i < x:
        order_obj = Order.objects.create(delivery=delivery_obj,
                                        full_name=address_list[i]["name"],
                                        tel_no=address_list[i]["tel_no"],
                                        address=address_list[i]["address"]
                                        )
        i = i + 1
    

    #
    #  Push Notification gönderiyor models - signals ile
    #


    serializer = DeliverySerializer(delivery_obj)

    return Response({'success': True,
                    'message': 'Başarıyla kaydedildi',
                    'response': {"delivery":serializer.data                
                    }},
                    status=HTTP_200_OK)






@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def update_delivery(request):
    print("-------------update delivery---------------")
    delivery_id = request.data.get("delivery_id")
    address_list = request.data.get("address_list")
    count = request.data.get("count")
    courier_id = request.data.get("courier_id")
    restaurant_id = request.data.get("restaurant_id")
    print(delivery_id)
    print(address_list)
    print(count)
    print(courier_id)
    print(restaurant_id)
    if not delivery_id or not address_list or not count  or not courier_id or not restaurant_id:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    print(kurye)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    # not: restorandan gelen bilgilere göre teslimat ve işlemleri düzenle(update) 
    
    delivery_obj = Delivery.objects.filter(id=delivery_id).first()
    if not delivery_obj:
        return Response({'success': False,
                         'message': 'Teslimat kaydı yok',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    delivery_obj.restaurant_id = restaurant_id
    delivery_obj.courier_id = courier_id
    delivery_obj.count = count
    delivery_obj.active_count = count
    delivery_obj.save()

    order_obj = Order.objects.filter(delivery=delivery_obj)
    if order_obj:
        for order in order_obj:
            order.delete()

    i = 0
    x = len(address_list)
    print("len", x)
    while i < x:
        order_obj = Order.objects.create(delivery=delivery_obj,
                                        full_name=address_list[i]["name"],
                                        tel_no=address_list[i]["tel_no"],
                                        address=address_list[i]["address"]
                                        )
        i = i + 1

    #
    # Push Notification gönderiyor models - signals ile
    #


    serializer = DeliverySerializer(delivery_obj)

    return Response({'success': True,
                    'message': 'Başarıyla güncellendi',
                    'response': {"delivery":serializer.data                
                    }},
                    status=HTTP_200_OK)





@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def delivery_approve_reject(request):
    print("-------------update delivery---------------")
    delivery_id = request.data.get("delivery_id")
    state = request.data.get("state")
    print(delivery_id)
    print(state)
    if not delivery_id or not state:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    # not: id'ye göre teslimat ve işlem bilgilerini al 
    
    delivery_obj = Delivery.objects.filter(id=delivery_id).first()
    if not delivery_obj:
        return Response({'success': False,
                         'message': 'Teslimat kaydı yok',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    order_obj = Order.objects.filter(delivery=delivery_obj)
    if not order_obj:
        return Response({'success': False,
                         'message': 'Teslimat sipariş kaydı yok',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    if state == 0:
        pass
        #  send notification to restaurant that delivery declined
        #  new order must be send

    else: 
        delivery_obj.confirm = True
        delivery_obj.save()

        kurye.state = "2"
        kurye.active_delivery = delivery_obj
        kurye.save()

        #  diğerlerinin sırası değişmeli....
        #   ...........................


    serializer = CourierSerializer(kurye)

    return Response({'success': True,
                    'message': 'Onaylandı',
                    'response': {"courier":serializer.data                
                    }},
                    status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def create_self_delivery(request):
    print("-------------create self delivery---------------")
    # sadece count gelecek ve kurye - serializer dönecek....
    #--------------------------------------------------------
    count = request.data.get("count")
    #courier_id = request.data.get("courier_id")
    #restaurant_id = request.data.get("restaurant_id")
    print(count)
    #print(courier_id)
    #print(restaurant_id)
    if  not count:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    print(kurye)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

  
    # not: restorandan gelen bilgilere göre yeni bir teslimat ve ilişkili işlemler yarat 
    print("teslimat yaratma öncesi")
    delivery_obj = Delivery.objects.create( 
                                        courier=kurye,
                                        restaurant=kurye.active_restaurant,
                                        count=count,
                                        active_count=count,
                                        confirm=True,
                                        self_delivery=True
                                        )
   
 
    i = 0
    x = int(count)
    print("len", x)
    while i < x:
        order_obj = Order.objects.create(delivery=delivery_obj,
                                        full_name="",
                                        tel_no="",
                                        address=""
                                        )
        i = i + 1
    

    kurye.state = "2"
    kurye.active_delivery = delivery_obj
    kurye.save()

    #  diğelerinin sırası değişmeli ...

    serializer = CourierSerializer(kurye)

    return Response({'success': True,
                    'message': 'Onaylandı',
                    'response': {"courier":serializer.data                
                    }},
                    status=HTTP_200_OK)











@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def delivery_process(request):
    print("-------------update delivery---------------")

    #  kurye serializer dönecek........................


    delivery_id = request.data.get("delivery_id")
    process_type_in = request.data.get("process_type")
    nondelivery_reason = request.data.get("nondelivery_reason")
    nonpayment_reason = request.data.get("nonpayment_reason")
    print(delivery_id)
    print(process_type_in)
    print(nondelivery_reason)
    print(nonpayment_reason)



    if not delivery_id or not process_type_in:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    # not: id'ye göre teslimat ve işlem bilgilerini al 
    
    delivery_obj = Delivery.objects.filter(id=delivery_id).first()
    if not delivery_obj:
        return Response({'success': False,
                         'message': 'Teslimat kaydı yok',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    
    order_x = Order.objects.filter(delivery=delivery_obj).filter(process_type="0")
    #order_y = order_x.filter(process_type="0")
    print("hepsi:",order_x)
    for order in order_x:
        print(order.pk)
    order_obj = order_x.first()
    print("ilk olan:",order_obj, order_obj.pk)
    if not order_obj:
        return Response({'success': False,
                         'message': 'Teslimat sipariş kaydı yok',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)
    

    #
    # burada gelen bilgiye göre teslimat işlemini gerçekleştir.
    # müşteriye SMS çek, SOS se teslimat dosyasında,
    # diğerlerinde ise Teslimat dosyasında kayıtları düzenle
    #

    if process_type_in == "1":
        print("case-1")
        order_obj.process_type = process_type_in
        order_obj.save()
        count = delivery_obj.active_count
        count = count -1
        delivery_obj.active_count = count
        delivery_obj.save()
        if count > 1: 
            # burada bir sonraki sıradaki kişiye SMS at
            pass
        else: 
            kurye.state = "3"
            kurye.save()

    elif process_type_in == "2":
        print("case-2")
        order_obj.process_type = process_type_in
        order_obj.non_payment_reason = nonpayment_reason
        order_obj.save()

        count = delivery_obj.active_count
        count = count -1
        delivery_obj.active_count = count
        delivery_obj.save()
        if count > 1: 
            # burada bir sonraki sıradaki kişiye SMS at
            pass
        else: 
            kurye.state = "3"
            kurye.save()


    elif process_type_in == "3":
        print("case-3")
        order_obj.process_type = process_type_in
        order_obj.non_delivery_reason = nondelivery_reason
        order_obj.save()

        count = delivery_obj.active_count
        count = count -1
        delivery_obj.active_count = count
        delivery_obj.save()
        if count > 1: 
            # burada bir sonraki sıradaki kişiye SMS at
            pass
        else: 
            kurye.state = "3"
            kurye.save()


    else:
        return Response({'success': False,
                         'message': 'İşlem tipi yanlış, kayıt dışı',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)
    


    serializer = CourierSerializer(kurye)

    return Response({'success': True,
                    'message': 'Onaylandı',
                    'response': {"courier":serializer.data                
                    }},
                    status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def quit_queue(request):
    print("-------------quit queue---------------")

    user = request.user
    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    # sadece sırada ise sıradan çıkmaya izin ver
    
    if kurye.state == "1":
        print("sırada")
        kurye.state = "4"
        kurye.save()
    else:
        return Response({'success': False,
                         'message': 'Kurye sırada değil!',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)
    

    #
    #  burada sıradan çıkma işleminin yapılması lazım 
    #

    serializer = CourierSerializer(kurye)
 
    return Response({'success': True,
                     'message': 'Başarılı',
                     'response' : {'courier': serializer.data }    
                    },
                    status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def enter_queue(request):
    print("-------------enter queue---------------")

    user = request.user
    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    # sadece sırada ise sıradan çıkmaya izin ver
    print(kurye.state)
 
    if  kurye.state == "4":
        print("sıradan çıkmış")
        kurye.state = "1"
        kurye.save()
    else:
        return Response({'success': False,
                         'message': 'Kurye sıradan çıkmış değil!',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)
    

    #
    #  burada sıraya girme işleminin yapılması lazım 
    #

    serializer = CourierSerializer(kurye)

    return Response({'success': True,
                     'message': 'Başarılı',
                     'response' : {'courier': serializer.data }    
                    },
                    status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def end_of_work(request):
    print("-------------end of work---------------")

    user = request.user
    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    # serviste değilken işi sonlandırmaya izin ver, servisteyken verme...
    
    if kurye.state != "2":
        print("iş bitiş")
        kurye.state = "0"
        kurye.save()
    else:
        return Response({'success': False,
                         'message': 'Servisteyken iş sonlandırılamaz!',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)
    


    serializer = CourierSerializer(kurye)

    return Response({'success': True,
                     'message': 'Başarılı',
                     'response' : {'courier': serializer.data }    
                    },
                    status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def sos(request):
    print("-------------SOS--------------")
    reason = request.data.get("reason")
    print(reason)
    if not reason:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)
                         
    user = request.user
    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : None
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)
    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)




    # sadece serviste ise SOS göndermeye izin ver
    
    if kurye.state == "2":
        print("SOS")
        kurye.state = "5"
        kurye.save()        
        delivery_obj = kurye.active_delivery
        if delivery_obj:
            delivery_obj.sos = True
            delivery_obj.sos_reason = reason
            delivery_obj.save()

    else:
        return Response({'success': False,
                         'message': 'Servis dışında SOS gönderilemez!',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)
    


    serializer = CourierSerializer(kurye)

    return Response({'success': True,
                     'message': 'SOS gerçekleşti',
                     'response' : {'courier': serializer.data }    
                    },
                    status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def sos_cancel(request):
    print("-------------SOS Cancel -------------")
    result = request.data.get("result")
    print(result)

    if not result:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    user = request.user
    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)

    kurye = Courier.objects.get(user_courier=user)

    if kurye.worker_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)


    # sadece SOS de ise sos_cancel gönder...
    
    if kurye.state == "5":
        print("SOS Cancel")
        kurye.state = "2"
        kurye.save()

        delivery_obj = kurye.active_delivery
        if delivery_obj:
            delivery_obj.sos = False
            delivery_obj.sos_result = result
            delivery_obj.save()

    else:
        return Response({'success': False,
                         'message': 'SOS durumunda değilsiniz!',
                         'response' : None,
                        },
                        status=HTTP_400_BAD_REQUEST)
    


    serializer = CourierSerializer(kurye)

    return Response({'success': True,
                     'message': 'Başarılı',
                     'response' : {'courier': serializer.data }    
                    },
                    status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def logout(request):
    try:
        uid = request.data.get('uid')
        print(uid)
        User=get_user_model()
        user = User.objects.get(pk=uid)
        print(user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        try:
            selected_token = Token.objects.get(user=user)
            selected_token.delete()
        except(Token.DoesNotExist):
            pass
        return Response({'token': ""}, status=HTTP_200_OK)
    else:
        return Response("error", status=HTTP_400_BAD_REQUEST)






class ReactAppView(View):

    def get(self, request):
        try:

            with open(os.path.join(settings.REACT_APP, 'build', 'index.html')) as file:
                return HttpResponse(file.read())

        except :
            return HttpResponse(
                """
                index.html not found ! build your React app !!
                """,
                status=501,
            )
# Create your views here.


