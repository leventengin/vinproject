
from rest_framework import viewsets
from django.conf import settings
from .models import User, AnaFirma, Firma
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
def login(request):
    print("-------------login---------------")
    username_or_email = request.data.get("username_or_email").rstrip()
    password = request.data.get("password")
    print(username_or_email)
    print(password)
    if not username_or_email or not password:
        return Response({'error': 'Lütfen kullanıcı adı ve parola girin'},
                        status=HTTP_400_BAD_REQUEST)
    
    if '@' in username_or_email:
        pass
    else:
        return Response({'error': 'Lütfen eposta hesabı giriniz'},
                        status=HTTP_400_BAD_REQUEST)

    User=get_user_model()

    try:
        user = User.objects.get(email=username_or_email)
    except:
        return Response({'error': 'Kullanıcı adı hatalı'},
                        status=HTTP_400_BAD_REQUEST)

    check_password = user.check_password(password)
    if not check_password:
        return Response({'error': 'Parola hatalı'},
                        status=HTTP_400_BAD_REQUEST)

    if user.is_active is False:
        return Response({'error': 'Hesap aktif değil'},
        status=HTTP_400_BAD_REQUEST)

    if user.aktif is False:
        return Response({'error': 'Hesap kapalı'},
        status=HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    
    print("here is pic_profile:", user.pic_profile)
    if user.pic_profile:
        pic_profile = BASE_URL + user.pic_profile.url
    else:
        pic_profile = ""
    return Response({'user_id': user.id, 'pic_profile': pic_profile, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'token': token.key, 'email': user.email}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def courier_login(request):
    print("-------------login_courier---------------")
    pin = request.data.get("pin")
    platform = request.data.get("device_platform")
    device_id = request.data.get("device_id")
    print(pin)
    print(platform)
    print(device_id)
    if not pin or not platform or not device_id:
        return Response({'success': 'false',
                        'message': 'Eksik bilgi gönderildi',
                        'courier': {}},
                        status=HTTP_400_BAD_REQUEST)

    User=get_user_model()
    try:
        user = User.objects.get(pin=pin)
    except:
        return Response({'success': 'false',
                        'message': 'Pin bulunamadı',
                        'courier': {}},
                        status=HTTP_400_BAD_REQUEST)

    if user.is_active is False:
        return Response({'success': 'false',
                        'message': 'Kullanıcı aktif değil',
                        'courier': {}},
                        status=HTTP_400_BAD_REQUEST)

    if user.aktif is False:
        return Response({'success': 'false',
                        'message': 'Kullanıcı aktif değil, silinmiş',
                        'courier': {}},
                        status=HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    print("here is pic_profile:", user.pic_profile)
    if user.pic_profile:
        pic_profile = BASE_URL + user.pic_profile.url
    else:
        pic_profile = ""
    return Response({'success': 'true',
                    'message': 'Başarılı login',
                    'courier': {'user_id': user.id,
                                'pic_profile': pic_profile,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'token': token.key,
                                'durum': user.durum}},
                    status=HTTP_200_OK)



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
def register(request):
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
def activate(request):
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
