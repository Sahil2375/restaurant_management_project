# Create your views here.
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ride, Driver
from .serializers import UpdateLocationSerializer, TrackRideSerializer
from .permissions import IsDriver, IsRideRiderOrAdmin
from django.shortcuts import get_object_or_404

# POST /api/ride/update-location/
class UpdateDriverLocation(APIView):
    permission_classes = [IsDriver]

    def post(self, request):
        serializer = UpdateLocationSerializer(data=request.data)
        if serializer.is_valid():
            driver = request.user.driver
            driver.current_latitude = serializer.validated_data['latitude']
            driver.current_longitude = serializer.validated_data['longitude']
            driver.save()
            return Response({"detail": "Location updated."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET /api/ride/track/<ride_id>/
class TrackRide(APIView):
    permission_classes = [IsRideRiderOrAdmin]

    def get(self, request, ride_id):
        ride = get_object_or_404(Ride, id=ride_id)

        # Check permission
        self.check_object_permissions(request, ride)

        # Only allow tracking if ride is ongoing
        if ride.status != 'ONGOING':
            return Response({"detail": "Ride is not ongoing."}, status=status.HTTP_403_FORBIDDEN)

        if not ride.driver:
            return Response({"detail": "Driver not assigned yet."}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "driver_latitude": ride.driver.current_latitude,
            "driver_longitude": ride.driver.current_longitude
        }
        serializer = TrackRideSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)