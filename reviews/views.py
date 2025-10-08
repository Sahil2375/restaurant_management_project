from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.db import DatabaseError
from .models import Review
from .serializers import ReviewSerializer

class ReviewPagination(PageNumberPagination):
    page_size = 10  # Customize how many reviews per page
    page_size_query_param = 'page_size'
    max_page_size = 50

class RestaurantReviewListView(ListAPIView):
    """
    API endpoint to retrieve all restaurant reviews.
    Supports pagination and graceful error handling.
    """
    queryset = Review.objects.all().order_by('created_at')
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

    # def get_queryset(self):
    #     restaurant_id = self.kwargs.get("restaurant_id")
    #     return Review.objects.filter(restaurant_id=restaurant_id).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except DatabaseError:
            return Response(
                {"error": "Database error occured while fetching reviews."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReviewListView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
