from django.shortcuts import render
from django.utils import timezone

# Create your views here.

def home(request):
    current_datetime = timezone.now()
    return render(request, 'home.html', {
        'current_datetime': current_datetime
    })