from django.contrib import admin
from .models import User, Firma, AnaFirma, Teslimat, IslemTeslimat, Bildirim, Bahsis, ArtiMotorcu
from .models import FaturaDetay, FaturaToplam, Fiyat, EkFiyat, Il, Ilce, Mahalle
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django import forms

# Kullanıcı seçme ekranı
class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        # Yeni model
        model = User

class MyUserAdmin(UserAdmin):
    # Yeni Form
    form = MyUserChangeForm
    # Görünmesi gerekenler
    list_display = UserAdmin.list_display+('durum',)
    search_fields = UserAdmin.search_fields+('durum',)
    # Yeni alanlar
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('tipi', 'durum', 'aktif_firma','sira', 'enlem', 'boylam', 'aktif', 'tel_no', 'pin', 'device_platform', 'device_id', 'pic_profile')}),
    )


#Yeni Kullanıcı oluşturma sınıfı
class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Yeni model
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


# MyUserAdmin sınıfı ile genişlettik.
admin.site.register(User, MyUserAdmin)# Register your models here.
admin.site.register(Firma)
admin.site.register(AnaFirma)
admin.site.register(Teslimat)
admin.site.register(IslemTeslimat)
admin.site.register(Bildirim)
admin.site.register(Bahsis)
admin.site.register(ArtiMotorcu)
admin.site.register(FaturaDetay)
admin.site.register(FaturaToplam)
admin.site.register(Fiyat)
admin.site.register(EkFiyat)
admin.site.register(Il)
admin.site.register(Ilce)
admin.site.register(Mahalle)

