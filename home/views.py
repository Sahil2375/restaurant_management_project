from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from .forms import FeedbackForm, ContactForm
from datetime import datetime

from .models import MenuItem, RestaurantInfo, Restaurant, TodaysSpecial, Chef

# Create your views here.

def homepage1(request):
    restaurant = RestaurantInfo.objects.first()  # Assuming only one entry
    specials = Special.objects.all()
    return render(request, 'homepage1.html', {'restaurant_info': restaurant_info}, {'specials': specials})

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
    
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, 'contact_success.html')  # Redirect after successful submission.

        else:
            form = ContactForm()
        return render(request, 'contact.html', {'form': form})

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
    menu_items = MenuItem.objects.all().order_by("name")  # fetch all items

    # Paginate with 5 items per page (you can change this)
    paginator = Paginator(menu_items, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'menu.html', {'page_obj': page_obj})

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

    #         # Send email to restaurnat
    #         subject = f"New contact submission from {contact.name}"
    #         message = f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}"
    #         from_email = settings.DEFAULT_FROM_EMAIL
    #         recipient_list = [settings.EMAIL_HOST_USER]  # Restaurant email

    #         send_mail(subject, message, from_email, recipient_list)

    #         return render(request, 'contact_success.html')

    # else:
    #     form = ContactForm()
    # return render(request, 'contact.html', {'form': form})

def about(request):
    # Display information about the restaurant, such as history and mission.
    context = {
        "restaurant_name": "Tasty Bites",
        "history": "Founded in 1998, Tasty Bites strats as a small family-run cafe and has grown into a beloved dining spotfor locals and tourist.",
        "mission": "To serve fresh, high-quality food with exceptional service, creating memorable dining experiences for all guests."
    }
    return render(request, "about.html", context)

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process data (e.g., save or send email).
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # You can save or send email here
            return render(request, "contact_success.html", {"name": name})
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})

def contact_us(request):
    restaurant = Restaurant.objects.first()  # Assuming only one restaurant
    return render(request, "contact_us.html", {"restaurant": restaurant})

def chef_view(request):
    chef = Chef.objects.first() # assuming only one main chef
    return render(request, "chef.html", {"chef": chef})