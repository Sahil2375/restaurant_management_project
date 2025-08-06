from django.shortcuts import render
from .models import Restaurant

# Create your views here.

def homepage(request):
    restaurant = Restaurant.objects.first()   # Fetch the first restaurant.
    restaurant_name = restaurant.name if restaurant else "Default Restaurant"
    return render(request, 'index.html', {'restaurant_name': restaurant.name})