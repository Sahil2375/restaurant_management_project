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
    list_display = ('id', 'customer', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username')
    filter_horizontal = ('order_items',) # For ManyToManyField Selection

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')

@admin.register(Special)
class SpecialAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price')

@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display = ('opening_hours',)