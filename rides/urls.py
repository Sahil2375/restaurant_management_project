# urls.py
from django.urls import path
from .views import UpdateDriverLocation, TrackRide, complete_ride, cancel_ride, RiderHistoryView, DriverHistoryView, RideFeedbackView, CalculateFareView

urlpatterns = [
    path('api/ride/update-location/', UpdateDriverLocation.as_view(), name='update-location'),
    path('api/ride/track/<int:ride_id>/', TrackRide.as_view(), name='track-ride'),
    path('api/ride/complete/<int:ride_id>/', complete_ride, name='complete-ride'),
    path('api/ride/cancel/<int:ride_id>/', cancel_ride, name='cancel-ride'),
    path('api/rider/history/', RiderHistoryView.as_view(), name='rider-history'),
    path('api/driver/history/', DriverHistoryView.as_view(), name='driver-history'),
    path('api/ride/feedback/<int:ride_id>/', RideFeedbackView.as_view(), name='ride-feedback'),
    path('api/ride/calculate-fare/<int:ride_id>/', CalculateFareView.as_view(), name='calculate-fare'),
]
