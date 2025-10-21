from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from .forms import FeedbackForm, ContactForm
from datetime import datetime

from django.http import HttpResponseForbidden, JsonResponse
from utils.validation_utils import is_valid_email

from .models import MenuItem, RestaurantInfo, Restaurant, TodaysSpecial, Chef, Table

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework import status, generics
from rest_framework import viewsets, filters, permissions
from rest_framework.pagination import PageNumberPagination

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from .models import MenuCategory, MenuItem, Rider, Driver, ContactFormSubmission, UserReview, Restaurant, OpeningHour, Menu, FAQ, Table, Cuisine, UserReview, Ingredient

from .serializers import RiderRegistrationSerializer, DriverRegistrationSerializer, MenuCategorySerializer, MenuItemAvailabilitySerializer, MenuItemSerializer, ContactFormSubmissionSerializer, DailySpecialSerializer, UserReviewSerializer, RestaurantSerializer, TableSerializer, OpeningHourSerializer, MenuItemSerializer, FAQSerializer, CuisineSerializer, UserReviewSerializer, IngredientSerializer

# Create your views here.

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
    

class MenuItemListView(ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.all()
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class MenuCategoryViewSet(viewsets.ViewSet):
    # queryset = MenuCategory.objects.all()
    # serializer_class = MenuCategorySerializer
    """
    A simple ViewSet for listing all menu categories.
    """
    def list(self, request):
        categories = MenuCategory.objects.all()
        serializer = MenuCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    # permission_classes = [permissions.IsAdminUser]  # Only admins can update

    def get_queryset(self):
        queryset = super().get_queryset()
        category_name = self.request.query_params.get('category')
        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)
            return queryset

    def partial_update(self, request, pk=None):
        """Handle PATCH requests (partial updates)."""
        menu_item = get_object_or_404(MenuItem, pk=pk)
        serializer = self.get_serializer(menu_item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class MenuItemAvailabilityView(APIView):
    """
    API endpoint to check the availability of a menu item by ID.
    """

    def get(self, request, pk):
        try:
            menu_item = MenuItem.objects.get(pk=pk)
            serializer = MenuItemAvailabilitySerializer(menu_item)
            return Response(
                {"available": menu_item.available, "item": serializer.data},
                status=status.HTTP_200_OK
            )
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "Menu item not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def register_user(request):
    email = request.POST.get('email', '')
    if not is_valid_email(email):
        return JsonResponse({'error': 'Invalid email address'}, status=400)
    
    # Continue with registration.
    return JsonResponse({'message': 'Email is valid'})


class MenuItemsByCuisineView(APIView):
    def get(self, request, cuisine_type):
        items = MenuItem.get_items_by_cuisine(cuisine_type)
        data = [{"id": item.id, "name": item.name, "price": item.price} for item in items]
        return Response({"cuisine": cuisine_type, "menu_items": data})


class ContactFormSubmissionView(CreateAPIView):
    queryset = ContactFormSubmission.objects.all()
    serializer_class = ContactFormSubmissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Contact form submitted successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DailySpecialListView(generics.ListAPIView):
    serializer_class = DailySpecialSerializer

    def get_queryset(self):
        # Only return items marked as daily specials
        return MenuItem.objects.filter(is_daily_special=True)
    
# Create new review
class CreateReviewView(generics.CreateAPIView):
    queryset = UserReview.objects.all()
    serializer_class = UserReviewSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users can review

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # assign the logged-in user automatically


# Retrieve reviews for a specific menu item
class MenuItemReviewsView(generics.ListAPIView):
    serializer_class = UserReviewSerializer
    permission_classes = [permissions.AllowAny]  # anyone can view reviews

    def get_queryset(self):
        menu_item_id = self.kwargs['menu_item_id']  # from URL
        return UserReview.objects.filter(menu_item_id=menu_item_id)


class UpdateMenuItemAvailability(APIView):
    def patch(self, request, pk):
        """
        Update availability of a MenuItem by ID.
        """
        menu_item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemAvailabilitySerializer(data=request.data)

        if serializer.is_valid():
            menu_item.is_available = serializer.validated_data["is_available"]
            menu_item.save()
            return Response(
                {
                    "message": f"Availability updated successfully for {menu_item.name}",
                    "menu_item": MenuItemSerializer(menu_item).data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantInfoView(APIView):
    def get(self, request):
        # Assuming there’s only ONE restaurant entry
        restaurant = Restaurant.objects.first()
        if not restaurant:
            return Response(
                {"error": "Restaurant information not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailableTablesAPIView(ListAPIView):
    """
    Returns a list of tables that are currently available.
    """
    serializer_class = TableSerializer

    def get_queryset(self):
        # Only return tables that are available
        return Table.objects.filter(is_available=True)

class TableDetailAPIView(RetrieveAPIView):
    """Retrieve details of a single table by its ID (pk)."""
    queryset = Table.objects.all()
    serializer_class = TableSerializer


@api_view(['GET'])
def search_menu_items(request):
    query = request.GET.get('q', '')  # Get 'q' parameter from query string
    if query:
        items = MenuItem.objects.filter(name__icontains=query)
    else:
        items = MenuItem.objects.none()  # Return empty if no query
    
    serializer = MenuItemSerializer(items, many=True, context={'request': request})
    return Response(serializer.data)


class OpeningHourListView(ListAPIView):
    queryset = OpeningHour.objects.all().order_by('id')
    serializer_class = OpeningHourSerializer

class MenuItemDetailView(APIView):
    def get(self, request, item_id):
        try:
            menu_item = Menu.objects.get(id=item_id)
        except Menu.DoesNotExist:
            return Response({"error": "Menu item not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data)
    

class MenuByPriceRangeView(ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        queryset = Menu.objects.all()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        try:
            if min_price is not None:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            if max_price is not None:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
        except ValueError:
            # Handle invalid input gracefully
            return Menu.objects.none()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return Response({"error": "Invalid price values provided."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RestaurantOpeningHoursView(APIView):
    def get(self, request):
        restaurant = Restaurant.objects.first()
        if not restaurant:
            return Response({"error": "Restaurant info not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"opening_hours": restaurant.opening_hours})


class FAQPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20


class FAQListView(generics.ListAPIView):
    """
    API endpoint to retrieve a list of frequently asked questions (FAQs).
    Supports pagination and handles empty datasets gracefully.
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]  # public endpoint
    pagination_class = FAQPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"message": "No FAQs available at the moment."},
                status=200
            )
        return super().list(request, *args, **kwargs)


class MenuItemCountView(APIView):
    """
    API endpoint to get total count of available menu items.
    """

    def get(self, request):
        # Count only available items
        total_items = MenuItem.objects.filter(is_available=True).count()
        return Response(
            {"total_menu_items": total_items},
            status=status.HTTP_200_OK
        )


class TableListAPIView(generics.ListAPIView):
    """
    API endpoint to list all tables.
    """
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class CuisineListView(generics.ListAPIView):
    """
    API endpoint to list all cuisine types.
    """
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer


class MenuItemReviewCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, menu_item_id):
        # Get menu item by ID
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)

        # Validate input
        serializer = UserReviewSerializer(data=request.data)
        if serializer.is_valid():
            # Save review linked to user and menu item
            serializer.save(user=request.user, menu_item=menu_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class ActiveMenuItemsView(generics.ListAPIView):
    """
    API view to list only active menu items.
    """
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        # Return only menu items where is_active is True
        return MenuItem.objects.filter(is_active=True)
