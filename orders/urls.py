from django.urls import path
from . import views
from .views import homepage_view, about_view, homepage_views

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('about/', about_view, name='about'),
    path('', views.homepage, name='homepage'),
    path('', homepage_views, name='home'),
]