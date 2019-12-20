from django.contrib import admin
from .models import User, Restaurant, Company, Delivery, Order, Notification, Tip, ExtraCourier
from .models import InvoiceDetail, InvoiceTotal, StandardPrice, AddedPrice, City, Town, District, Courier
from .models import WSClients
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
    list_display = UserAdmin.list_display+('user_type',)
    search_fields = UserAdmin.search_fields+('user_type',)
    # Yeni alanlar
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('user_type', 'pic_profile',)}),
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
admin.site.register(Restaurant)
admin.site.register(Company)
admin.site.register(Delivery)
admin.site.register(Order)
admin.site.register(Courier)
admin.site.register(Notification)
admin.site.register(Tip)
admin.site.register(ExtraCourier)
admin.site.register(InvoiceTotal)
admin.site.register(InvoiceDetail)
admin.site.register(StandardPrice)
admin.site.register(AddedPrice)
admin.site.register(City)
admin.site.register(Town)
admin.site.register(District)
admin.site.register(WSClients)

