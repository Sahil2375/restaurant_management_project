from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Review
from .serializers import ReviewSerializer

class ReviewPagination(PageNumberPagination):
    page_size = 5  # default items per page
    page_size_query_param = 'page_size'
    max_page_size = 20

class RestaurantReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

    def get_queryset(self):
        restaurant_id = self.kwargs.get("restaurant_id")
        return Review.objects.filter(restaurant_id=restaurant_id).order_by('-created_at')
