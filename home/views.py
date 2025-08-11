from django.shortcuts import render, redirect
from .forms import FeedbackForm, ContactForm
from datetime import datetime
from .models import MenuItem

from .models import Restaurant

# Create your views here.

def homepage1(request):
    return render(request, 'homepage1.html', {
        'current_year' : datetime.now().year
    })
    
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