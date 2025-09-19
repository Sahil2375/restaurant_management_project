# urls.py
from django.urls import path
from .views import UpdateDriverLocation, TrackRide

urlpatterns = [
    path('api/ride/update-location/', UpdateDriverLocation.as_view(), name='update-location'),
    path('api/ride/track/<int:ride_id>/', TrackRide.as_view(), name='track-ride'),
]
