from django.contrib import admin
from .models import RestaurantInfo, TodaysSpecial

# Register your models here.

admin.site.register(RestaurantInfo)

admin.site.register(TodaysSpecial)