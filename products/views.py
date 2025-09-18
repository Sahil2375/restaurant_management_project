# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.decorators import api_view
# from django.conf import settings

# from .models import Item
# from .serializers import ItemSerializer

# '''
# NOTE: Conside this as a reference and follow this same coding structure or format to work on you tasks
# '''

# # Create your views here.
# class ItemView(APIView):

#     def get(self, request):
#         items = Item.objects.all()
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = ItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def menu_list(request):
#     """
#     Api endpoint to retrieve the restaurant's menu.
#     Currently returns hardcoded data for simplicity
#     """
#     menu = [
#         {
#             "name": "Margherita Pizza",
#             "description": "Classic pizza with tomato sauce, mozzarella, and fresh basil.",
#             "price": 9.99
#         },
#         {
#             "name": "Paneer Tikka",
#             "description": "Classic panner with spicicy tikki",
#             "price": 6.5
#         },
#         {
#             "name": "Veg Biryani",
#             "description": "Classic biryani with good quality basmati rice",
#             "price": 8.2
#         }
#     ]
#     return Response(menu)

# def homepage(request):
#     # Display the homepage with the restaurant name.
#     {
#         'restaurant_name': settings.RESTAURANT_NAME,
#         'some_other_key': 'some_value',
#     }
#     return render(request, 'homepage.html')


# def menu_list_view(request):
#     return render(request, "products/menu_list.html")

# def contact_us_view(request):
#     return render(request, "products/contact_us.html")

# def reservations_view(request):
#     return render(request, "products/reservations.html")


from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseServerError

# Example ItemView if you plan to use class-based views
from django.views import View

# Temporary hardcoded menu items
MENU_ITEMS = [
    {'name': 'Margherita Pizza', 'price': 300},
    {'name': 'Paneer Tikka', 'price': 250},
    {'name': 'Veg Biryani', 'price': 200},
    {'name': 'Masala Dosa', 'price': 100},
]

# Function-based views
def menu_list_view(request):
    return render(request, 'menu_list.html', {'menu_items': MENU_ITEMS})

def contact_us_view(request):
    contact_info = {
        'phone': '+91-9987545643',
        'email': 'contact@restaurant.com',
        'address': '540 Main Street, Mumbai, Maharashtra, India'
    }
    return render(request, 'contact_us.html', {'contact': contact_info})

def reservations_view(request):
    return render(request, 'reservations.html')

# Optional: Class-based view example
class ItemView(View):
    def get(self, request):
        return render(request, 'item_list.html', {'menu_items': MENU_ITEMS})