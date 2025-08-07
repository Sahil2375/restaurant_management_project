from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from 

from .models import Item
from .serializers import ItemSerializer

'''
NOTE: Conside this as a reference and follow this same coding structure or format to work on you tasks
'''

# Create your views here.
class ItemView(APIView):

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def menu_list_view(request):
        # Hardcoded list of menu items
        menu_items = [
            {'name': 'Margherita pizza', 'price': 300},
            {'name': 'Paneer Tikka', 'price': 250},
            {'name': 'Veg Biryani', 'price': 200},
            {'name': 'Masala dosa', 'price': 100},
        ]
        return render(request, 'menu_list.html', {'menu_items': menu_items})

    def contact_us_view(request):
        contact_info = {
            'phone': '+91-9987545643',
            'email': 'my@resto.com',
            'address': '540, Main Street, Mumbai, Maharashtra, India'
        }
        return render(request, 'contact_us.html', {'contact': contact_info})