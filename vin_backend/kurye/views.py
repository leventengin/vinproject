
from rest_framework import viewsets
from django.conf import settings
from .models import User, AnaFirma, Firma, WSClient
from .serializers import UserSerializer, AnaFirmaSerializer, FirmaSerializer
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



def _pw(length=10):
    s = ''
    for i in range(length):
        s += random.choice(string.ascii_letters + string.digits)
    return s




class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    User = get_user_model()
    queryset = User.objects.all()

class AnaFirmaViewSet(viewsets.ModelViewSet):
    serializer_class = AnaFirmaSerializer
    queryset = AnaFirma.objects.all()

class FirmaViewSet(viewsets.ModelViewSet):
    serializer_class = FirmaSerializer
    queryset = Firma.objects.all()





@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def pin_login(request):
    print("-------------pin login---------------")
    pin = request.data.get("pin").rstrip()
    
    user_agent = get_user_agent(request)
    print("user-agent")
    print(user_agent)

    print(pin)
    if not pin:
        return Response({'success': False,
                         'message': 'Pin girilmemiş',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)
    
    User=get_user_model()

    try:
        user = User.objects.get(pin=pin)
    except:
        return Response({'success': False,
                         'message': 'Pin tanımlı değil',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    if user.aktif is False:
        return Response({'success': False,
                         'message': 'Hesap kapalı',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)
    
    new_password = _pw()
    #print("new password", new_password)
    user.set_password(new_password)
    user.save()

    print(user.username, '/', user.password)
    #json_data = JsonResponse({'username':user.username, 'password': user.password})
    json_data = {'username':user.username, 'password': new_password}
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
    username_or_email = request.data.get("username_or_email").rstrip()
    password = request.data.get("password")
    print(username_or_email)
    print(password)
    if not username_or_email or not password:
        return Response({'success': False,
                         'message': 'Lütfen kullanıcı adı ve parola giriniz',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)
    
    if '@' in username_or_email:
        pass
    else:
        return Response({'success': False,
                         'message': 'Lütfen eposta hesabı giriniz',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)
    User=get_user_model()

    try:
        user = User.objects.get(email=username_or_email)
    except:
        return Response({'success': False,
                         'message': 'Kullanıcı adı hatalı',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    check_password = user.check_password(password)
    if not check_password:
        return Response({'success': False,
                         'message': 'Parola hatalı',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Hesap aktif değil',
                         'response' : {
                            'courier_status': ''
                         }},
                         status=HTTP_400_BAD_REQUEST)

    if user.aktif is False:
        return Response({'success': False,
                         'message': 'Hesap kapalı',
                         'response' : {
                            'courier_status': ''
                         }},
                         status=HTTP_400_BAD_REQUEST)


    
    print("here is pic_profile:", user.pic_profile)
    if user.pic_profile:
        pic_profile = BASE_URL + user.pic_profile.url
    else:
        pic_profile = ""
    return Response({'success': True,
                    'message': 'Başarılı login',
                    'response': {
                        'restaurant':
                            {
                                'user_id': user.id, 
                                'pic_profile': pic_profile, 
                                'username': user.username, 
                                'first_name': user.first_name, 
                                'last_name': user.last_name,  
                                'email': user.email}, 
                            }
                    },
                    status=HTTP_200_OK)





@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def courier_get_self_data(request):
    print("-------------login_courier---------------")

    user = request.user
    print(user)

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    if user.aktif is False:
        return Response({'success': False,
                         'message': 'Kullanıcı silinmiş',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

 
    print("here is pic_profile:", user.pic_profile)
    if user.pic_profile:
        pic_profile = BASE_URL + user.pic_profile.url
    else:
        pic_profile = ""
    return Response({'success': True,
                    'message': 'Başarılı login',
                    'response':{
                            'courier': { 'user_id': user.id,
                                         'pic_profile': pic_profile,
                                         'first_name': user.first_name,
                                         'last_name': user.last_name,
                                         'durum': user.durum}
                    }},
                    status=HTTP_200_OK)




"""
@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def send_location(request):
    print("-------------send location---------------")
    token = request.data.get("token")
    latitude = request.data.get("latitude")
    longitude = request.data.get("longitude")
    print(token)
    print(latitude)
    print(longitude)
    if not token or not latitude or not longitude:
        return Response({'success': 'false',
                        'message': 'Eksik bilgi gönderildi',
                        'courier_status': ''},
                        status=HTTP_400_BAD_REQUEST)

    try:
        token_obj = Token.objects.get(key=token)
    except:
        return Response({'success': 'false',
                        'message': 'Token bulunamadı',
                        'courier_status': ''},
                        status=HTTP_400_BAD_REQUEST)

    user = token_obj.user

    if user.is_active is False:
        return Response({'success': 'false',
                        'message': 'Kullanıcı aktif değil',
                        'courier_status': ''},
                        status=HTTP_400_BAD_REQUEST)

    if user.aktif is False:
        return Response({'success': 'false',
                        'message': 'Kullanıcı aktif değil, silinmiş',
                        'courier_status': ''},
                        status=HTTP_400_BAD_REQUEST)

    #token, created = Token.objects.get_or_create(user=user)

    user.enlem = latitude
    user.boylam = longitude
    user.save()

    return Response({'success': 'true',
                    'message': 'Başarılı',
                    'courier_status': user.durum},
                    status=HTTP_200_OK)
"""



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
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    if user.aktif is False:
        return Response({'success': False,
                         'message': 'Kullanıcı silinmiş',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    # en yakındaki restoranları listele, yoksa boş dön
    # kayıtlı değilse kayıtlı değil bilgisi dönüyor
    # not: şu an için hepsini dönüyor, test döneminde bu şekilde 
    
    rest_list = get_rest_list(latitude=latitude, longitide=longitude, user_id=user.id)

    return Response({'success': True,
                     'message': 'Başarılı',
                     'response' : {
                        'restorant_list': rest_list
                     }},
                    status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def select_restorant(request):
    print("---------select restorant---------------")
    rest_id = request.data.get("rest_id")
    print(rest_id)
    if not rest_id:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)


    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kullanıcı aktif değil',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    if user.aktif is False:
        return Response({'success': False,
                         'message': 'Kullanıcı silinmiş',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    User=get_user_model() 
    rest_obj =  User.objects.filter(id=rest_id).first()
    firma_adi = rest_obj.firma_adi
    tel_no = rest_obj.tel_no
    if rest_obj.allow_self_delivery:
        allow_self_delivery = "true"
    else:
        allow_self_delivery = "false"

    yeni_sira = siraya_gir(rest_obj.id)
    user_obj.sira = yeni_sira
    user_obj.aktif_firma = rest_obj.id
    user_obj.save()


    return Response({'success': True,
                     'message': 'Başarılı',
                     'response' : {
                         'restaurant': {
                            'restaurant_name': firma_adi,
                            'tel_no': tel_no,
                            'allow_self_delivery': allow_self_delivery,
                            'queue_order_courier': yeni_sira
                         }
                     }},
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
    prit(user_obj.username)

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
    firma_obj = Firma.objects.filter(id=token_obj.user).first()

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
    firma_obj = Firma.objects.filter(id=token_obj.user).first()

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
    print(address_list)
    print(count)
    print(courier_id)
    if not address_list or not count  or not courier_id:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    if user.aktif is False:
        return Response({'success': False,
                         'message': 'Kullanıcı silinmiş',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)


    # not: restorandan gelen bilgilere göre yeni bir teslimat ve ilişkili işlemler yarat 
    
    tesl_obj = Teslimat.objects.create( firma=user,
                                        kurye_id=courier_id,
                                        adet=count,
                                        gecerli_adet=count
                                        )

    for address in address_list:
        islem_obj = IslemTeslimat.objects.create(teslimat=tesl_obj,
                                                tel_no=address.tel_no,
                                                address=address.address
                                                )


    #
    # sonrasında Push Notification gönder.....
    #


    return Response({'success': True,
                     'message': 'Başarılı',
                     'response' : {
                        'delivery_id': tesl_obj.id
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
    print(delivery_id)
    print(address_list)
    print(count)
    print(courier_id)
    if not delivery_id or not address_list or not count  or not courier_id:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    if user.aktif is False:
        return Response({'success': False,
                         'message': 'Kullanıcı silinmiş',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)


    # not: restorandan gelen bilgilere göre teslimat ve işlemleri düzenle(update) 
    
    tesl_obj = Teslimat.objects.filter(id=delivery_id).first()
    if not tesl_obj:
        return Response({'success': False,
                         'message': 'Teslimat kaydı yok',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)


    tesl_obj = Teslimat.objects.save(id=delivery_id,
                                        firma=user,
                                        kurye_id=courier_id,
                                        adet=count,
                                        gecerli_adet=count
                                        )

    islem_obj = IslemTeslimat.objects.filter(teslimat=tesl_obj)
    if islem_obj:
        for islem in islem_obj:
            islem.delete()

    for address in address_list:
        islem_obj = IslemTeslimat.objects.create(teslimat=tesl_obj,
                                                tel_no=address.tel_no,
                                                address=address.address
                                                )


    #
    # sonrasında Push Notification gönder.....
    #


    return Response({'success': True,
                     'message': 'Başarılı',
                     'response' : {
                        'delivery_id': tesl_obj.id
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
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    if user.aktif is False:
        return Response({'success': False,
                         'message': 'Kullanıcı silinmiş',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)


    # not: id'ye göre teslimat ve işlem bilgilerini al 
    
    tesl_obj = Teslimat.objects.filter(id=delivery_id).first()
    if not tesl_obj:
        return Response({'success': False,
                         'message': 'Teslimat kaydı yok',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)


    islem_obj = IslemTeslimat.objects.filter(teslimat=tesl_obj)
    if not islem_obj:
        return Response({'success': False,
                         'message': 'Teslimat detay kaydı yok',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    address_list = {}
    address_item = {}

    for islem in islem_obj:
        address_item = {"process_id": islem.id, 
                        "address": islem.address, 
                        "tel_no": islem.tel_no,}
        address_list.append(address_item)

    print(address_list)

    return Response({'success': True,
                     'message': 'Başarılı',
                     'response' : {
                        'address_list': address_list,
                        'count': tesl_obj.adet,
                     }},
                    status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def delivery_process(request):
    print("-------------update delivery---------------")
    delivery_id = request.data.get("delivery_id")
    process_id = request.data.get("process_id")
    process_id_next = request.data.get("process_id_next")    
    restaurant_id = request.data.get("restaurant_id")
    process_type = request.data.get("process_type")
    nondelivery_reason = request.data.get("nondelivery_reason")
    nonpayment_reason = request.data.get("nonpayment_reason")
    sos_reason = request.data.get("sos_reason")
    soscancel_result = request.data.get("soscancel_result")
    print(delivery_id)
    print(process_id)
    print(process_id_next)
    print(restaurant_id)
    print(process_type)
    print(nondelivery_reason)
    print(nonpayment_reason)
    print(sos_reason)
    print(soscancel_result)


    if not delivery_id or not process_id or not restaurant_id or not process_type:
        return Response({'success': False,
                         'message': 'Eksik bilgi gönderildi',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    user = request.user

    if user.is_active is False:
        return Response({'success': False,
                         'message': 'Kulanıcı aktif değil',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    if user.aktif is False:
        return Response({'success': False,
                         'message': 'Kullanıcı silinmiş',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)


    # not: id'ye göre teslimat ve işlem bilgilerini al 
    
    tesl_obj = Teslimat.objects.filter(id=delivery_id).first()
    if not tesl_obj:
        return Response({'success': False,
                         'message': 'Teslimat kaydı yok',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)


    islem_obj = IslemTeslimat.objects.filter(id=process_id).first()
    if not islem_obj:
        return Response({'success': False,
                         'message': 'Teslimat detay kaydı yok',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)

    #
    # burada gelen bilgiye göre teslimat işlemini gerçekleştir.
    # müşteriye SMS çek, SOS se teslimat dosyasında,
    # diğerlerinde ise Teslimat dosyasında kayıtları düzenle
    #

    if process_type == "1":
        print("case-1")
        islem_obj.islem_tipi = process_type
        islem_obj.save()
        count = tesl_obj.adet
        count = count -1
        tesl_obj.adet = count
        tesl_obj.save()
        if count > 1: 
            # burada bir sonraki sıradaki kişiye SMS at
            pass
        else: 
            user.durum = "3"
            user.save()

    elif process_type == "2":
        print("case-2")
        islem_obj.islem_tipi = process_type
        islem_obj.odeme_alinmadi_sebep = nonpayment_reason
        islem_obj.save()
        count = tesl_obj.adet
        count = count -1
        tesl_obj.adet = count
        tesl_obj.save()
        if count > 1: 
            # burada bir sonraki sıradaki kişiye SMS at
            pass
        else: 
            user.durum = "3"
            user.save()


    elif process_type == "3":
        print("case-3")
        islem_obj.islem_tipi = process_type
        islem_obj.teslim_edilmedi_sebep = nondelivery_reason
        islem_obj.save()
        count = tesl_obj.gecerli_adet
        count = count -1
        tesl_obj.gecerli_adet = count
        tesl_obj.save()
        if count > 1: 
            # burada bir sonraki sıradaki kişiye SMS at
            pass
        else: 
            user.durum = "3"
            user.save()



    elif process_type == "4":
        print("case-4")
        islem_obj.islem_tipi = process_type
        islem_obj.sos_sebep = sos_reason
        islem_obj.save()
        user.durum = "4"
        user.save()
        #
        # burada çalışılan restorana bildirim at
        #

    elif process_type == "5":
        print("case-4")
        islem_obj.islem_tipi = process_type
        islem_obj.sos_kaldir_sonuc = soscancel_result
        islem_obj.save()
        user.durum = "5"
        user.save()
        #
        # burada çalışılan restorana bildirim at
        #

    else:
        return Response({'success': False,
                         'message': 'İşlem tipi yanlış, kayıt dışı',
                         'response' : {
                         }},
                         status=HTTP_400_BAD_REQUEST)
    


    return Response({'success': True,
                     'message': 'Başarılı',
                     'response' : {
                        'courier_state': user.durum,
                        'package_count': tesl_obj.adet,
                     }},
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


