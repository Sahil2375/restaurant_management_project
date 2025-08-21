from django.urls import path, include
from django.contrib import admin
from django.shortcuts import render
from . import views

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', views.homepage, name='homepage1'),
    path('', views.home_view, name='home'),
    path('reservations/', views.reservations, name='reseravtions'),
    path('our_story/', views.our_story_view, name='our_story'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu_view, name='menu'),
]

handler404 = 'home.urls.custom_404_view'