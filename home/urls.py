from django.urls import path, include
from django.contrib import admin
from django.shortcuts import render
from . import views
from .views import RiderRegisterView, DriverRegisterView

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', views.homepage, name='homepage1'),
    path('', views.home_view, name='home'),
    path('reservations/', views.reservations, name='reseravtions'),
    path('our_story/', views.our_story_view, name='our_story'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu_view, name='menu'),
    path("gallery/", views.gallery, name="gallery"),
    path("api/rider/register/", RiderRegisterView.as_view(), name="rider-register"),
    path("api/driver/register/", DriverRegisterView.as_view(), name="driver-register"),
]

handler404 = 'home.urls.custom_404_view'