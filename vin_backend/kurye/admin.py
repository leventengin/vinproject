from django.contrib import admin
from .models import User, AnaFirma
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
            (None, {'fields': ('durum',)}),
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
admin.site.register(AnaFirma)
