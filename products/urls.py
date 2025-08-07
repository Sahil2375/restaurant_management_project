from django.urls import path
from .views import menu_list_view, contact_us_view

urlpatterns = [
    path('items/', ItemView.as_view(), name='item-list'),
    path('menu/', menu_list_view, name='menu-list'),
    path('contact', contact_us_view, name='contact-us'),
]