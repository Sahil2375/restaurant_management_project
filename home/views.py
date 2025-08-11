from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import FeedbackForm, ContactForm
from datetime import datetime
from .models import MenuItem, RestaurantInfo

from .models import Restaurant

# Create your views here.

def homepage1(request):
    restaurant = RestaurantInfo.objects.first()  # Assuming only one entry
    return render(request, 'homepage1.html', {'restaurant' : restaurant})
    
def homepage(request):
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

        return render(request, 'feedback.html', {
            'form': form,
            'current_year': datetime.now().year
        })

def menu_view(request):
    # Display all menu items on the menu page.
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Send email to restaurnat
            subject = f"New contact submission from {contact.name}"
            message = f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.EMAIL_HOST_USER]  # Restaurant email

            send_mail(subject, message, from_email, recipient_list)

            return render(request, 'contact_success.html')

    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})