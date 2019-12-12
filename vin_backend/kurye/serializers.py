from rest_framework import serializers
from .models import User, AnaFirma, Firma, Teslimat, IslemTeslimat
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        #fields = ('first_name', 'last_name', 'email', 'username', 'durum')


class AnaFirmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnaFirma
        fields = '__all__'


class FirmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firma
        fields = '__all__'


class IslemTeslimatSerializer(serializers.ModelSerializer):
    class Meta:
        model = IslemTeslimat
        fields = '__all__'


class TeslimatSerializer(serializers.ModelSerializer):
    islemteslimats = IslemTeslimatSerializer(many=True, read_only=True)
    class Meta:
        model = Teslimat
        fields = ['kurye', 'firma', 'onay', 'adet', 'gecerli_adet', 'islemteslimats']




