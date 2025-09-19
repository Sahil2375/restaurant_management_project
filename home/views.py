from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from .forms import FeedbackForm, ContactForm
from datetime import datetime

from django.http import HttpResponseForbidden, JsonResponse
from utils.validation_utils import is_valid_email

from .models import MenuItem, RestaurantInfo, Restaurant, TodaysSpecial, Chef

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, filters, permissions
from rest_framework.pagination import PageNumberPagination

from rest_framework.generics import ListAPIView
from .models import MenuCategory, MenuItem, Rider, Driver

from .serializers import RiderRegistrationSerializer, DriverRegistrationSerializer, MenuCategorySerializer, MenuItemSerializer

# Create your views here.

def homepage1(request):
    restaurant = RestaurantInfo.objects.first()  # Assuming only one entry
    specials = TodaysSpecial.objects.all()
    opening_hours = {
        "Monday": "9:00 AM - 10:00 PM",
        "Tuesday": "9:00 AM - 10:00 PM",
        "Wednesday": "9:00 AM - 10:00 PM",
        "Thrusday": "9:00 AM - 10:00 PM",
        "Friday": "9:00 AM - 11:00 PM",
        "Saturday": "10:00 AM - 11:00 PM",
        "Sunday": "Closed",
    }

    context = {
        "restaurant_info": restaurant,
        "specials": specials,
        "opening_hours": opening_hours,
        "current_year": datetime.now().year,
        "page_title": "Welcome to Tasty Bites Restaurant - Best Dining in Mumbai",
    }

    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage1')  # Reload page after success
    else:
        form = SubscriberForm()
        
    return render(request, 'homepage1.html', {
        'restaurant_info': restaurant_info,
        'specials': specials, 
        "opening_hours": opening_hours,
        "current_year": datetime.now().year
    }, context)

def reservations(request):
    return render(request, "reservations.html", {
        "current_year": datetime.now().year
    })

def reservations_view(request):
    return render(request, 'reservations.html')


def about_us(request):
    return render(request, "about_us.html", {
        "current_year": datetime.now().year
    })

def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)

    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1
    else:
        cart[str(item_id)] = {
            'name': item.name,
            'price': float(item.price),
            'quantity': 1
        }
        
    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'cart.html', {'cart': cart, 'total': total})
    
def homepage(request):
    query = request.GET.get('q', '')  # Get search term from URL
    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)  # Case-insensitive match
    else:
        menu_items = MenuItem.objects.all()

    # Get cart count fron sessions
    cart = request.session.get('cart', [])
    cart_count = len(cart)

    return render(request, 'homepage.html', {
        'menu_items': menu_items,
        'query': query,
        'cart_count': cart_count
    })
    
    return redirect('contact_success')


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback')  # Redirect after saving.

        else:
            form = FeedbackForm()

        return render(request, 'feedback.html', {'form': form})

def menu_view(request):

    # Paginate with 5 items per page (you can change this)

    query = request.GET.get('q')  # Get search term from query params
    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)  # Case-insensitive match
    else:
        menu_items = MenuItem.objects.all()

    paginator = Paginator(menu_items, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'menu.html', {
        'page_obj': page_obj,
        'menu_items': menu_items, 'query':query
        })

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # or handle sending email, saving to DB, etc.
            messages.success(request, "Thank You, your message has been sent!")
            return redirect("contact") # stay on the contact page
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})

def about(request):
    # Display information about the restaurant, such as history and mission.
    context = {
        "restaurant_name": "Tasty Bites",
        "history": "Founded in 1998, Tasty Bites strats as a small family-run cafe and has grown into a beloved dining spotfor locals and tourist.",
        "mission": "To serve fresh, high-quality food with exceptional service, creating memorable dining experiences for all guests."
    }
    return render(request, "about.html", context)

def contact(request):

    return render(request, "contact.html")

def contact_us(request):
    restaurant = Restaurant.objects.first()  # Assuming only one restaurant
    return render(request, "contact_us.html", {"restaurant": restaurant})

def chef_view(request):
    chef = Chef.objects.first() # assuming only one main chef
    return render(request, "chef.html", {"chef": chef})

def our_story_view(request):
    return render(request, 'our_story.html')

def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')

def staff(request):
    return render(request, 'staff.html')

def index(request):
    restaurant = RestaurantInfo.objects.first()  # fetch first record
    return render(request, "home/index.html", {"restaurant": restaurant})

def custom_403(request, exception=None):
    return render(request, '403.html', status=403)

def secret_view(request):
    return HttpResponseForbidden()

def gallery(request):
    images = [
        "https://picsum.photos/400/300?random=1",
        "https://picsum.photos/400/300?random=2",
        "https://picsum.photos/400/300?random=3",
        "https://picsum.photos/400/300?random=4",
    ]
    return render(request, "home/gallery.html", {"images": images})



class RiderRegisterView(APIView):
    def post(self, request):
        serializer = RiderRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            rider = serializer.save()
            return Response(serializer.to_representation(rider), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverRegisterView(APIView):
    def post(self, request):
        serializer = DriverRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            driver = serializer.save()
            return Response(serializer.to_representation(driver), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuCategoryListAPIView(ListAPIView):
    """
    API endpoint that allows menu categories to be viewed.
    """
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

class MenuItemPagination(PageNumberPagination):
    page_size = 10 # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    # pagination_class = MenuItemPagination
    permission_classes = [permissions.IsAdminUser]  # Only admins can update

    def update(self, request, pk=None):
        menu_item = get_object_or_404(MenuItem, pk=pk)
        serializer = self.get_serializer(menu_item, data=request.data, partial=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """Handle PATCH requests (partial updates)."""
        menu_item = get_object_or_404(MenuItem, pk=pk)
        serializer = self.get_serializer(menu_item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     search_query = self.request.query_params.get('q', None)
    #     if search_query:
    #         queryset = queryset.filter(name__icontains=search_query)
    #     return queryset


class MenuItemsByCategoryView(APIView):
    """
    Retrieve menu items filtered by category name.
    Example: /menu-items-by-category/?category=Pizza
    """

    def get(self, request, *args, **kwargs):
        category_name = request.query_params.get("category", None)

        if not category_name:
            return Response(
                {"error": "Category parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        items = MenuItem.objects.filter(category__category_name__iexact=category_name)

        if not items.exists():
            return Response(
                {"message": f"No items found for category '{category_name}'"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def register_user(request):
    email = request.POST.get('email', '')
    if not is_valid_email(email):
        return JsonResponse({'error': 'Invalid email address'}, status=400)
    
    # Continue with registration.
    return JsonResponse({'message': 'Email is valid'})