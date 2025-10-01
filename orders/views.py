from django.shortcuts import render
from .models import Restaurant, Order
from datetime import datetime
from django.conf import settings
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
import requests

from home.models import MenuItem

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .models import Order, Coupon, MenuCategory
from .serializers import OrderSerializer, UpdateOrderStatusSerializer, MenuCategorySerializer

from orders.utils import send_order_confirmation_email, send_email


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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=["delete"], url_path="cancel")
    def cancel_order(self, request, pk=None):
        """Cancel an order by setting its status to 'Cancelled'."""
        order = get_object_or_404(Order, pk=pk)

        # (Optional) Add logic to check if the user owns the order
        # if order.customer != request.user:
        #     return Response({"error": "You can only cancel your own orders."}, status=403)

        if order.status == "Cancelled":
            return Response({"message": "Order is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = "Cancelled"
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class OrderConfirmationView(APIView):
    def post(self, request, *args, **kwargs):
        customer_email = request.data.get("email")
        order_id = request.data.get("order_id")

        subject = f"Order #{order_id} Confirmation"
        body = f"Thank you for your order! Your order ID is {order_id}."

        if send_email(customer_email, subject, body):
            return Response({"message": "Confirmation email sent."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateOrderStatusView(APIView):
    def post(self, request):
        serializer = UpdateOrderStatusSerializer(data=request.data)
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            new_status = serializer.validated_data['status']

            try:
                order = Order.objects.get(order_id=order_id)
            except Order.DoesNotExist:
                return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
            
            order.status = new_status
            order.save()
            return Response({"message": "Order status updated successfully.", "order_id": order.order_id, "new_status": order.status})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UpdateOrderStatusAPIView(APIView):
    """
    API view to update the status of an existing order.
    """

    def put(self, request, order_id):
        serializer = UpdateOrderStatusSerializer(data=request.data)
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            new_status = serializer.validated_data['status']

            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

            order.status = new_status
            order.save()
            return Response({
                'message': 'Order status updated successfully',
                'order_id': order.id,
                'status': order.status
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_order_status(request, order_id):
    """
    Retrieve the current status of an order by ID.
    """
    try:
        order = Order.objects.get(id=order_id)
        return Response(
            {"order_id": order.id, "status": order.status},
            status=status.HTTP_200_OK
        )
    except Order.DoesNotExist:
        return Response(
            {"error": f"Order with ID {order_id} not found."},
            status=status.HTTP_404_NOT_FOUND
        )


class CouponValidationView(APIView):
    """
    Validate a coupon code.
    """
    def post(self, request):
        code = request.data.get("code", "").strip()

        if not code:
            return Response(
                {"error": "Coupon code is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return Response(
                {"error": "Invalid coupon code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not coupon.is_valid():
            return Response(
                {"error": "Coupon is inactive or expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Coupon is valid.",
                "code": coupon.code,
                "discount_percentage": float(coupon.discount_percentage)
            },
            status=status.HTTP_200_OK
        )

class MenuCategoryListView(ListAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer