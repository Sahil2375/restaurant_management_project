from django.contrib import admin
from .models import RestaurantInfo, MenuItem

# Register your models here.

@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')