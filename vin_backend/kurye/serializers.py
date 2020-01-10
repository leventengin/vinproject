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
                'pk',
                'username',
                'first_name', 
                'last_name', 
                'email', 
                'user_type', 
                'pic_profile',
                'pic_profile_abs_url',
                'pic_map',
                'pic_map_abs_url',                
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
                    'company',
                    'tel_no', 
                    'second_tel',
                    'allow_self_delivery', 
                    'latitude',
                    'longitude',
                    'registered_couriers',
                    'active_couriers',
                    'address',
                    'district',
                    'town',
                    'city',
                ]



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    order_delivery = OrderSerializer(many=True, read_only=True)
    class Meta:
        model = Delivery
        fields = [  
                    'pk',
                    'courier', 
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
    #user_courier = UserSerializer(read_only=True)
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    pic_profile = serializers.SerializerMethodField()
    pic_profile_abs_url = serializers.SerializerMethodField()
    latitude = serializers.DecimalField(max_digits=16, decimal_places=12, coerce_to_string=False)
    longitude = serializers.DecimalField(max_digits=16, decimal_places=12,  coerce_to_string=False)
    class Meta:
        model = Courier
        fields = [  
                    'pk', 
                    'username',
                    'first_name', 
                    'last_name', 
                    'email', 
                    'user_type', 
                    'pic_profile',
                    'pic_profile_abs_url',
                    'state', 
                    'queue', 
                    'latitude', 
                    'longitude', 
                    'active_restaurant',
                    'active_delivery',
                    'active_order',
                    'worker_active',
                    'tel_no',
                    'device_platform',
                    'device_id',
                    'registered_restaurants',
                    'city',
                    'town',
                    'district',
                    'address',
                    'own_motocycle'
                ]        
    def get_username(self,obj):
        return obj.user_courier.username
    def get_first_name(self,obj):
        return obj.user_courier.first_name
    def get_last_name(self,obj):
        return obj.user_courier.last_name       
    def get_email(self,obj):
        return obj.user_courier.email
    def get_user_type(self,obj):
        return obj.user_courier.user_type
    def get_pic_profile(self,obj):
        if obj.user_courier.pic_profile:
            return obj.user_courier.pic_profile.url
        else:
            return None
    def get_pic_profile_abs_url(self,obj):
        if obj.user_courier.pic_profile:
            return obj.user_courier.pic_profile_abs_url
        else:        
            return None




class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
                'username',
                'pic_profile',
                ]




class RestSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    pic_profile = serializers.SerializerMethodField()
    pic_profile_abs_url = serializers.SerializerMethodField()
    latitude = serializers.DecimalField(max_digits=16, decimal_places=12, coerce_to_string=False)
    longitude = serializers.DecimalField(max_digits=16, decimal_places=12,  coerce_to_string=False)
    class Meta:
        model = Restaurant
        fields = [  
                    'pk', 
                    'username',
                    'first_name', 
                    'last_name', 
                    'email', 
                    'user_type', 
                    'pic_profile',
                    'pic_profile_abs_url',
                    'name', 
                    'company', 
                    'tel_no', 
                    'second_tel', 
                    'allow_self_delivery',
                    'registered_couriers',
                    'active_couriers',
                    'address',
                    'district',
                    'town',
                    'city',
                    'latitude',
                    'longitude'
                ]   

    def get_username(self,obj):
        return obj.user_restaurant.username
    def get_first_name(self,obj):
        return obj.user_restaurant.first_name
    def get_last_name(self,obj):
        return obj.user_restaurant.last_name       
    def get_email(self,obj):
        return obj.user_restaurant.email
    def get_user_type(self,obj):
        return obj.user_restaurant.user_type
    def get_pic_profile(self,obj):
        if obj.user_restaurant.pic_profile:
            return obj.user_restaurant.pic_profile.url
        else:
            return None
    def get_pic_profile_abs_url(self,obj):
        if obj.user_restaurant.pic_profile:
            return obj.user_restaurant.pic_profile_abs_url
        else:        
            return None




