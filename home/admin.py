from django.contrib import admin
from .models import RestaurantInfo, MenuItem, Feedback, Chef, Table, MenuCategory, DailyOperatingHours, Staff, Allergen

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
    list_display = ('table_number', 'capacity', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('table_number',)

admin.site.register(DailyOperatingHours)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role', 'contact_email')
    list_filter = ('role',)
    search_fields = ('first_name', 'last_name', 'contact_email')

admin.site.register(Allergen)