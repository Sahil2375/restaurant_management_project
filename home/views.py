from django.shortcuts import render
from .models import Restaurant
from django.conf import settings

# Create your views here.

def homepage_view(request):
    restaurant = Restaurant.objects.first()   # Fetch the first restaurant.
    return render(request, 'Homepage.html', {'restaurant_name': restaurant.name if restaurant else 'Restaurant'})