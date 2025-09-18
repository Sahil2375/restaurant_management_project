from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Login route using Django's built-in LoginView
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='home.html'),
        name='login'
    ),
]