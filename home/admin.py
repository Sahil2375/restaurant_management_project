from django.contrib import admin
from .models import RestaurantInfo, MenuItem, Feedback, Chef, Table, MenuCategory

# Register your models here.

@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'feedback_text', 'submitted_at')

@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(MenuCategory)

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('number',)