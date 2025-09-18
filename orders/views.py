from django.shortcuts import render
from .models import Restaurant
from datetime import datetime
from django.conf import settings
from django.http import HttpResponseServerError
import requests

# Homepage view that fetches menu items from API
def homepage(request):
    try:
        response = requests.get('http://localhost:8000/api/menu/')
        menu_items = response.json() if response.status_code == 200 else []
    except Exception:
        menu_items = []

    return render(request, 'homepage.html', {'menu_items': menu_items})


# Hardcoded menu list
def menu_list_view(request):
    menu_items = [
        {'name': 'Margherita Pizza', 'price': 300},
        {'name': 'Paneer Tikka', 'price': 250},
        {'name': 'Veg Biryani', 'price': 200},
        {'name': 'Masala Dosa', 'price': 100},
    ]
    return render(request, 'menu_list.html', {'menu_items': menu_items})


# Contact page
def contact_us_view(request):
    contact_info = {
        'phone': '+91-9987545643',
        'email': 'my@resto.com',
        'address': '540 Main Street, Mumbai, Maharashtra, India'
    }
    return render(request, 'contact_us.html', {'contact': contact_info})


# Homepage showing restaurant name from database
def homepage_views(request):
    try:
        restaurant = Restaurant.objects.first()
        restaurant_name = restaurant.name if restaurant else "Our Restaurant"
    except Exception:
        return HttpResponseServerError("An unexpected error occurred. Please try again later.")

    context = {
        'restaurant_name': restaurant_name,
        'welcome_message': 'Welcome To Tasty Bites! Experience delicious food and warm hospitality',
        'current_year': datetime.now().year
    }
    return render(request, 'Home.html', context)


# Homepage view that fetches restaurant info
def homepage_view(request):
    try:
        # Assume only one Restaurant instance exists
        restaurant = Restaurant.objects.first()
        restaurant_name = restaurant.name if restaurant else "Our Restaurant"
        context = {
            'restaurant_name': restaurant_name,
            'welcome_message': 'Welcome To {}! Enjoy our delicious food.'.format(restaurant_name),
            'current_year': datetime.now().year
        }
        return render(request, 'home.html', context)

    except Exception as e:
        return HttpResponseServerError("An unexpected error occurred: {}".format(e))


# About page
def about_view(request):
    return render(request, 'orders/about.html')


# Reservations page
def reservations_view(request):
    return render(request, 'reservations.html')
