from django.urls import path
from .views import RestaurantReviewListView

urlpatterns = [
    path('reviews/', RestaurantReviewListView.as_view(), name='restaurant-reviews'),
]
