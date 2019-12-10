from django.conf import settings
from .models import User, Firma
from django.contrib.auth import get_user_model
import math



def calculate_distance(latitude, longitude, rest_latitude, rest_longitude ):
    print("longitude", longitude)
    print("latitude", latitude)
    print("rest_longitude", rest_longitude)
    print("rest_latitude", rest_latitude)   
    # iki lokasyon arasındaki uzaklığı hesapla - HAVERSINE

    R = 6372800  # Earth radius in meters
    
    phi1, phi2 = math.radians(latitude), math.radians(rest_latitude) 
    dphi       = math.radians(rest_latitude - latitude)
    dlambda    = math.radians(rest_longitude - longitude)
    
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

    rest_obj = User.objects.filter(tipi="1")
    list_rest = []

    for rest_inst  in rest_obj: 
        distance = calculate_distance(latitude, longitude, rest_inst.enlem, rest_inst.boylam)
        #motorcu o restorana kayıtlı mı bak
        kayitlilar = rest_inst.kayitli_motorcular
        kayitli = False
        if rest_inst.id in kayitlilar:
            kayitli = True
        arr_item = {"id": rest_inst.id, 
                    "restorant_name": rest_inst.firma.firma_adi, 
                    "tel_no": rest_obj.firma.tel_no,
                    "distance": distance, 
                    "kayitli": kayitli }
        list_rest.append(arr_item)
    
    print("list_rest")
    print(list_rest)
    list_rest.sort(key = lambda x: x.distance)
    print("------------")
    print(list_rest)
    return list_rest



# returns the last+1 number in the queue
# this is the number to be given to the new courier in the database field
# while changing its status to -3 which means in the queue

def siraya_gir(firma_id):
    print("siraya_gir")
    print(firma_id)
    User=get_user_model()
    motorcu_obj =  User.objects.filter(aktif_firma=firma_id).filter(durum="3").order_by('sira')
    print(motorcu_obj)
    sira = 0
    if motorcu_obj:
        last_motorcu = motorcu_obj.last()
        sira = int(last_motorcu.sira)
    sira = sira+1
    return sira




# this is different from siraya_gir
# updates the database fields of related courier and other couriers in the queue
# updating the model KayitliMotorcular
# it does not update the  status of related courier, it must be done in calling function 

def siradan_cik(firma_id, motorcu_id, sira):
    print("siradan_cik")
    print(firma_id)
    print(motorcu_id) 
    print(sira) 
    User=get_user_model()
    motorcu_obj =  User.objects.filter(aktif_firma=firma_id).filter(durum="3")
    for motorcu in motorcu_obj:
        if motorcu.sira > sira:
            sayi = int(motorcu.sira)
            sayi = sayi - 1
            motorcu.sira = str(sayi)
            motorcu.save()
    return None







