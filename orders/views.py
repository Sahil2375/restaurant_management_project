from django.shortcuts import render
from .models import Restaurant

from django.conf import settings

# Create your views here.

def homepage(request):
    restaurant = Restaurant.objects.first()  # Fetch the first restaurant
    return render(request, 'index.html', {'restaurant_name': restaurant.name if restaurant else 'Restaurant'})

def menu_list_view(request):
    # harcoded list of menu items
    menu_items = [
        {'name': 'Margherita Pizza', 'price': 300},
        {'name': 'Paneer Tikka', 'price': 250},
        {'name': 'Veg Biryani', 'price': 200},
        {'name': 'Masala Dosa', 'price': 100},
    ]
    return render(request, 'menu_list.html', {'menu_items': menu_items})

def contact_us_view(request):
    contact_info = {
        'phone': '+91-9987545643',
        'email': 'my@resto.com',
        'address': '540 Main Street, Mumbai, Maharashtra, India'
    }
    return render(request, 'contact_us.html', {'contact': contact_info})

def homepage_view(request):
    phone_number = settings.RESTAURANT_PHONE

    return render(request, 'home.html', {'phone': phone_number})

def homepage_views(request):
    context = {
        'restaurant_name': 'Tasty Bites',
        'welcome_message': 'Welcome To Tasty Bites! Experience delicious food and warm hospitality',
    }
    return render(request, 'Home.html', context)