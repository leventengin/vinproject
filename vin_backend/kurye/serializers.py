from rest_framework import serializers
from .models import User, Company, Restaurant, Delivery, Order, Courier
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.contrib.auth import get_user_model






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        #fields = '__all__'
        fields = [
                'username',
                'first_name', 
                'last_name', 
                'email', 
                'user_type', 
                'pic_profile',
                'pic_profile_abs_url',
                ]
 



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [  
                    'pk',
                    'name', 
                    'tel_no', 
                    'allow_self_delivery', 
                    'latitude',
                    'longitude',
                    'registered_couriers'
                ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    order_delivery = OrderSerializer(many=True, read_only=True)
    class Meta:
        model = Delivery
        fields = [  'courier', 
                    'restaurant', 
                    'confirm', 
                    'count', 
                    'active_count', 
                    'sos',
                    'sos_reason',
                    'sos_result',
                    'timestamp',
                    'order_delivery'
                ]



class CourierSerializer(serializers.ModelSerializer):
    active_restaurant = RestaurantSerializer(read_only=True)
    active_delivery = DeliverySerializer(read_only=True)
    active_order = OrderSerializer(read_only=True)
    user_courier = UserSerializer(read_only=True)
    class Meta:
        model = Courier
        fields = [  
                    'user_courier', 
                    'state', 
                    'queue', 
                    'latitude', 
                    'longitude', 
                    'active_restaurant',
                    'active_delivery',
                    'active_order',
                    'active_worker',
                    'tel_no',
                    'device_platform',
                    'device_id',
                    'registered_restaurants'
                ]        


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
                'username',
                'pic_profile',
                ]






