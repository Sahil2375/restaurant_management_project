from django.shortcuts import render
from .models import Restaurant
from datetime import datetime

from django.conf import settings
from django.http import HttpResponseServerError

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
    """
    Display the homepage with the restaurant name.

    This view fetches the restaurant name from the database and renders it on the homepage.
    If a database error or any unexpected issue occurs, it handles the error gratefully
    and returns an error page or message.
    """
    try:
        # Assume there is only one Restaurant entry.
        restaurant = Restaurant.objects.first()
        restaurant_name = restaurant.name if restaurant else "Our Restaurant"

        return render(request, 'Home,html', {'restaurant_name': restaurant_name})

    except Expection as e:
        # Log the error if needed (e.g., using logging module)
        # import logging
        # logger = logging.getLogger(__name__)
        # logger.error("Error loading homepage: %s", e)

        return HttpResponseServerError("An unexpected error occured. Please try again later.")
    
    context = {
        'restaurant_name': 'Tasty Bites',
        'welcome_message': 'Welcome To Tasty Bites! Experience delicious food and warm hospitality',
        'current_year': datetime.now().year
    }
    return render(request, 'Home.html', context)

def reservations_view(request):
    return render(request, 'reservations.html')