# urls.py
from django.urls import path
from .views import UpdateDriverLocation, TrackRide, complete_ride, cancel_ride

urlpatterns = [
    path('api/ride/update-location/', UpdateDriverLocation.as_view(), name='update-location'),
    path('api/ride/track/<int:ride_id>/', TrackRide.as_view(), name='track-ride'),
    path('api/ride/complete/<int:ride_id>/', complete_ride, name='complete-ride'),
    path('api/ride/cancel/<int:ride_id>/', cancel_ride, name='cancel-ride'),
]
