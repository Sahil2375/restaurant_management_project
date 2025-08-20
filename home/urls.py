from django.urls import path, include
from django.contrib import admin
from django.shortcuts import render
from . import views

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', views.homepage, name='homepage'),
]

handler404 = 'home.urls.custom_404_view'