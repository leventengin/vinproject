
from rest_framework import viewsets
from django.conf import settings
from .models import User, AnaFirma
from .serializers import UserSerializer, AnaFirmaSerializer

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







class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class AnaFirmaViewSet(viewsets.ModelViewSet):
    serializer_class = AnaFirmaSerializer
    queryset = AnaFirma.objects.all()




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
    """
    if '@' in username_or_email:
        kwargs = {'email': username_or_email}
    else:
        kwargs = {'username': username_or_email}
    """
    kwargs = {'username': username_or_email}
    try:
        user = User.objects.get(**kwargs)
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


