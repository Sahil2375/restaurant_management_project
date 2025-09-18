# from django.urls import path
# from .views import menu_list_view, contact_us_view, reservations_view, ItemView

# urlpatterns = [
#     path('items/', ItemView.as_view(), name='item-list'),
#     path('menu/', menu_list_view, name='menu-list'),
#     path('contact', contact_us_view, name='contact-us'),
#     path('reservations/', reservations_view, name='reservations'),
# ]

from django.urls import path
from .views import menu_list_view, contact_us_view, reservations_view, ItemView

urlpatterns = [
    path('menu/', menu_list_view, name='menu-list'),
    path('contact/', contact_us_view, name='contact-us'),
    path('reservations/', reservations_view, name='reservations'),
    path('items/', ItemView.as_view(), name='item-list'),  # class-based view
]