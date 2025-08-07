from django.shortcuts import render
from .models import Restaurant

from django.conf import settings

# Create your views here.

def homepage(request):
    restaurant = Restaurant.objects.first()  # Fetch the first restaurant
    return render(request, 'index.html', {'restaurant_name': restaurant.name if restaurant else 'Restaurant'})

def 

def homepage_view(request):
    phone_number = settings.RESTAURANT_PHONE
    return render(request, 'home.html', {'phone': phone_number})