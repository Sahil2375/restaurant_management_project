from django.urls import path
from .views import RestaurantReviewListView

urlpatterns = [
    path('restaurant/<int:restaurant_id>/reviews/', RestaurantReviewListView.as_view(), name='restaurant-reviews'),
]
