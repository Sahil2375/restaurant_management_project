from django.urls import path
from .views import RestaurantReviewListView, ReviewListView

urlpatterns = [
    path('reviews/', RestaurantReviewListView.as_view(), name='restaurant-reviews'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
]
