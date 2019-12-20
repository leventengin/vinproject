from django.conf import settings
from .models import Courier, Restaurant
from django.contrib.auth import get_user_model
import math
from decimal import Decimal
from .serializers import RestaurantSerializer


def calculate_distance(latitude, longitude, rest_latitude, rest_longitude ):
    print("longitude", longitude)
    print("latitude", latitude)
    print("rest_longitude", rest_longitude)
    print("rest_latitude", rest_latitude)   
    # iki lokasyon arasındaki uzaklığı hesapla - HAVERSINE
    new_latitude = Decimal(latitude)
    new_longitude = Decimal(longitude)

    R = 6372800  # Earth radius in meters
    
    phi1, phi2 = math.radians(new_latitude), math.radians(rest_latitude) 
    dphi       = math.radians(rest_latitude - new_latitude)
    dlambda    = math.radians(rest_longitude - new_longitude)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    distance = 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    print("distance", distance)

    return distance





def get_rest_list(latitude, longitude, user_id):
    print("get_rest_list")
    print("longitude", longitude)
    print("latitude", latitude)

    User=get_user_model()

    rest_obj = Restaurant.objects.all()
    list_rest = []

    for rest_inst  in rest_obj: 
        distance = calculate_distance(latitude, longitude, rest_inst.latitude, rest_inst.longitude)
        #motorcu o restorana kayıtlı mı bak
        print("---distance---")
        print(rest_inst.name, "distance", distance)
        #kayitlilar = rest_inst.kayitli_motorcular
        #kayitli = False
        #if user_id in kayitlilar:
        #    kayitli = True

        serializer = RestaurantSerializer(rest_inst)
        arr_item = serializer.data
        list_rest.append(arr_item)
   
    #list_rest.sort(key = lambda x: x['distance'])
    print(list_rest)
    return list_rest



# returns the last+1 number in the queue
# this is the number to be given to the new courier in the database field
# while changing its status to -3 which means in the queue

def siraya_gir(rest_id):
    print("siraya_gir")
    print(rest_id)
    motorcu_obj =  Courier.objects.filter(active_restaurant=rest_id).filter(state="1")
    print(motorcu_obj)
    sira = motorcu_obj.count() + 1
    print("sira----",sira)
    return sira




# this is different from siraya_gir
# updates the database fields of related courier and other couriers in the queue
# updating the model KayitliMotorcular
# it does not update the  status of related courier, it must be done in calling function 

def siradan_cik(rest_id, courier_id, sira):
    print("siradan_cik")
    print(rest_id)
    print(courier_id) 
    print(sira) 
    User=get_user_model()
    motorcu_obj =  User.objects.filter(active_restaurant=rest_id).filter(state="3")
    for motorcu in motorcu_obj:
        if motorcu.queue > sira:
            sayi = motorcu.queue
            sayi = sayi - 1
            motorcu.queue = sayi
            motorcu.save()
    return None







