from django.urls import path
from .views import (
    homepage,
    menu_list_view,
    contact_us_view,
    homepage_view,
    homepage_views,
    reservations_view,
    about_view
)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('menu/', menu_list_view, name='menu-list'),
    path('contact/', contact_us_view, name='contact-us'),
    path('home/', homepage_view, name='home-view'),
    path('home-db/', homepage_views, name='home-db-view'),
    path('reservations/', reservations_view, name='reservations'),
    path('about/', about_view, name='about'),
]