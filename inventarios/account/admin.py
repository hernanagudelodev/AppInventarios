from django.contrib import admin
from .models import Profile, Inmobiliaria

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']

@admin.register(Inmobiliaria)
class InmobiliariaAdmin(admin.ModelAdmin):
    list_display = ['nombre','email','telefono']

