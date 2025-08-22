from django.shortcuts import render
from django.utils import timezone

# Create your views here.

def home(request):
    current_datetime = timezone.now()
    return render(request, 'home.html', {
        'current_datetime': current_datetime
    })

def restaurant_gallery(request):
    images = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        "https://example.com/image3.jpg",
        "https://example.com/image4.jpg",
    ]
    return render(request, "restaurant/gallery.html", {"images": images})