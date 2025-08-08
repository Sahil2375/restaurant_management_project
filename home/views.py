from django.shortcuts import render, redirect
from .forms import FeedbackForm
from datetime import datetime

from .models import Restaurant

# Create your views here.

def homepage(request):
    restaurant = Restaurant.objects.first()   # Fetch the first restaurant.
    restaurant_name = restaurant.name if restaurant else "Default Restaurant"
    return render(request, 'index.html', {'restaurant_name': restaurant.name})

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