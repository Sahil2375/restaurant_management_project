from django.contrib import admin
from .models import Menu, Order, UserProfile, Special, RestaurantInfo

# Register your models here.

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)
    list_filter = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)

    def get_total_amount(self, obj):
        return obj.total_price
    get_total_amount.short_description = 'Total Amount'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')

@admin.register(Special)
class SpecialAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price')

@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display = ('opening_hours',)