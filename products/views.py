from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings

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

@api_view(['GET'])
def menu_list(request):
    """
    Api endpoint to retrieve the restaurant's menu.
    Currently returns hardcoded data for simplicity
    """
    menu = [
        {
            "name": "Margherita Pizza",
            "description": "Classic pizza with tomato sauce, mozzarella, and fresh basil.",
            "price": 9.99
        },
        {
            "name": "Paneer Tikka",
            "description": "Classic panner with spicicy tikki",
            "price": 6.5
        },
        {
            "name": "Veg Biryani",
            "description": "Classic biryani with good quality basmati rice",
            "price": 8.2
        }
    ]
    return Response(menu)

def homepage(request):
    # Display the homepage with the restaurant name.
    context = {
        'restaurant_name' = settings.RESTAURANT_NAME
    }
    return render(request, 'homepage.html', context)