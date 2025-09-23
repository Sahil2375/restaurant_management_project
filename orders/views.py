from django.shortcuts import render
from .models import Restaurant, Order
from datetime import datetime
from django.conf import settings
from django.http import HttpResponseServerError
import requests

from home.models import MenuItem

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from .serializers import OrderSerializer

from orders.utils import send_order_confirmation_email


# Homepage view that fetches menu items from API
def homepage(request):
    try:
        menu_items = MenuItem.objects.all()
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


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
def place_order(request):
    # Assume order created successfully
    order_id = 123
    customer_email = "customer@example.com"
    customer_name = "Nathen Ruth"

    result = send_order_confirmation_email(order_id, customer_email, customer_name)
    print(result)  # { "success": True, "message": "Email sent successfully." } or { "success": False, "message": "Error details..." }

class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'  # URL will match by 'id'