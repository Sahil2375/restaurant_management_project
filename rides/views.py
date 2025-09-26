# Create your views here.
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Ride, Driver
from .serializers import UpdateLocationSerializer, TrackRideSerializer, RideHistorySerializer, RideFeedbackSerializer, FareCalculationSerializer
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
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_ride(request, ride_id):
    """Driver marks ride as completed."""
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

    # Rule 1: Only assigned driver can complete
    if ride.driver != request.user:
        return Response({"error": "You are not assigned to this ride."}, status=status.HTTP_403_FORBIDDEN)

    # Rule 2: Ride must be ongoing
    if ride.status != "ONGOING":
        return Response({"error": "Ride can only be completed if it is ongoing."}, status=status.HTTP_400_BAD_REQUEST)

    ride.status = "COMPLETED"
    ride.save()
    return Response({"message": "Ride marked as completed."}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_ride(request, ride_id):
    """Rider cancels ride if still requested."""
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

    # Rule 1: Only rider who booked can cancel
    if ride.rider != request.user:
        return Response({"error": "You are not the rider of this ride."}, status=status.HTTP_403_FORBIDDEN)

    # Rule 2: Can only cancel if still requested
    if ride.status != "REQUESTED":
        return Response({"error": "Cannot cancel a ride that is already ongoing or completed."}, status=status.HTTP_400_BAD_REQUEST)

    ride.status = "CANCELLED"
    ride.save()
    return Response({"message": "Ride cancelled successfully."}, status=status.HTTP_200_OK)

class RiderHistoryView(generics.ListAPIView):
    serializer_class = RideHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ride.objects.filter(
            rider=self.request.user,
            status__in=['COMPLETED', 'CANCELLED']
        ).order_by('-created_at')
    
class DriverHistoryView(generics.ListAPIView):
    serializer_class = RideHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ride.objects.filter(
            driver=self.request.user,
            status__in=['COMPLETED', 'CANCELLED']
        ).order_by('-created_at')
    
class RideFeedbackView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, ride_id):
        serializer = RideFeedbackSerializer(
            data=request.data, 
            context={"request": request, "ride_id": ride_id}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Feedback submitted successfully."}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CalculateFareView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        # Get the ride
        ride = get_object_or_404(Ride, id=ride_id)

        # Ensure only rider, driver, or admin can access
        if not (
            request.user == ride.rider
            or request.user == ride.driver
            or request.user.is_staff
        ):
            return Response(
                {"message": "You do not have permission to calculate fare for this ride."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        # Ensure ride is completed
        if ride.status != "COMPLETED":
            return Response(
                {"message": "Ride must be completed before fare calculation"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Prevent recalculation
        if ride.fare is not None:
            return Response(
                {"message": "Fare already set.", "fare": float(ride.fare)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Use serializer to calculate and save fare
        serializer = FareCalculationSerializer(ride, context={"request": request})
        fare = serializer.save()

        return Response(
            {"fare": fare, "message": "Fare calculated and saved."},
            status=status.HTTP_200_OK
        )
