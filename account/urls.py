from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserProfileUpdateView, StaffListView

urlpatterns = [
    # Login route using Django's built-in LoginView
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('api/staff/', StaffListView.as_view(), name='staff-list'),
]