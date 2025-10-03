# serializers.py
from rest_framework import serializers
from .models import Ride, Driver, RideFeedback
from .utils import calculate_distance
from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum, Count, Avg
from datetime import timedelta

class UpdateLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

class TrackRideSerializer(serializers.Serializer):
    driver_latitude = serializers.FloatField()
    driver_longitude = serializers.FloatField()

class RideHistorySerializer(serializers.ModelSerializer):
    driver = serializers.CharField(source="driver.username", allow_null=True)
    rider = serializers.CharField(source="rider.username", read_only=True)

    class Meta:
        model = Ride
        fields = ['id', 'rider', 'driver', 'pickup', 'drop', 'status', 'created_at']

class RideFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideFeedback
        fields = ["rating", "comment"]

    def validate(self, data):
        request = self.context.get["request"]
        ride_id = self.context.get("ride_id")

        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            raise serializers.ValidationError({"error": "Ride not found."})
        
        # Rule 1: Ride must be completed
        if ride.status != "COMPLETED":
            raise serializers.ValidationError({"error": "Ride is not completed yet."})

        # Rule 2: User must belong to the ride
        user = request.user
        if ride.rider != user and ride.driver != user:
            raise serializers.ValidationError({"error": "You are not part of this ride."})

        # Determine role
        is_driver = (ride.driver == user)

        # Rule 3: Check if feedback already exists
        if RideFeedback.objects.filter(ride=ride, is_driver=is_driver).exists():
            raise serializers.ValidationError({"error": "Feedback already submitted."})

        # Save info for create()
        self.context["ride"] = ride
        self.context["is_driver"] = is_driver

        return data

    def create(self, validated_data):
        ride = self.context["ride"]
        user = self.context["request"].user
        is_driver = self.context["is_driver"]

        feedback = RideFeedback.objects.create(
            ride=ride,
            submitted_by=user,
            is_driver=is_driver,
            **validated_data
        )
        return feedback


class FareCalculationSerializer(serializers.ModelSerializer):
    surge_multiplier = serializers.FloatField(default=1.0, write_only=True)  # allow client to send surge

    class Meta:
        model = Ride
        fields = ['id', 'pickup_lat', 'pickup_lon', 'drop_lat', 'drop_lon', 'status', 'fare', 'surge_multiplier']
        read_only_fields = ['fare']

    def validate(self, data):
        """
        Prevent fare calculation if ride not completed or already has fare.
        """
        ride = self.instance
        if ride.status != "COMPLETED":
            raise serializers.ValidationError("Fare can only be calculated for completed rides.")
        if ride.fare is not None:
            raise serializers.ValidationError("Fare already calculated for this ride.")
        return data

    def update(self, instance, validated_data):
        """
        Calculate and store fare for the ride.
        """
        # Constants
        base_fare = Decimal(50)
        per_km_rate = Decimal(10)

        surge_multiplier = Decimal(str(validated_data.get('surge_multiplier', 1.0)))

        # Distance
        distance = Decimal(str(
            calculate_distance(instance.pickup_lat, instance.pickup_lon, instance.drop_lat, instance.drop_lon)
        )).quantize(Decimal("0.01"))

        # Fare calculation
        fare = base_fare + (distance * per_km_rate * surge_multiplier)

        # Save fare
        instance.fare = fare.quantize(Decimal("0.01"))
        instance.save()

        return instance

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['payment_method', 'payment_status']

    def validate(self, data):
        ride = self.instance  # serializer is used with an existing Ride instance

        # ✅ Ensure ride is completed
        if ride.status != "COMPLETED":
            raise serializers.ValidationError("Ride must be completed before payment.")

        # ✅ Prevent double payment
        if ride.payment_status == "PAID":
            raise serializers.ValidationError("Payment already completed for this ride.")

        # ✅ Only allow PAID or UNPAID
        if data.get("payment_status") not in ["PAID", "UNPAID"]:
            raise serializers.ValidationError("Invalid payment status.")

        # ✅ If marking as PAID, payment_method is required
        if data.get("payment_status") == "PAID" and not data.get("payment_method"):
            raise serializers.ValidationError("Payment method is required when marking as PAID.")

        return data

    def update(self, instance, validated_data):
        instance.payment_status = validated_data.get("payment_status", instance.payment_status)
        instance.payment_method = validated_data.get("payment_method", instance.payment_method)

        # ✅ If marked PAID, set paid_at timestamp
        if instance.payment_status == "PAID" and not instance.paid_at:
            instance.paid_at = timezone.now()

        instance.save()
        return instance
    

class DriverEarningsSummarySerializer(serializers.Serializer):
    total_rides = serializers.IntegerField()
    total_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_breakdown = serializers.DictField(child=serializers.IntegerField())
    average_fare = serializers.DecimalField(max_digits=10, decimal_places=2)

    @classmethod
    def from_driver(cls, driver):
        now = timezone.now()
        week_ago = now - timedelta(days=7)

        # Filter relevant rides
        rides = Ride.objects.filter(
            driver=driver,
            status="COMPLETED",
            payment_status="PAID",
            completed_at__gte=week_ago
        )

        # Aggregate
        total_rides = rides.count()
        total_earnings = rides.aggregate(total=Sum("fare"))["total"] or 0
        average_fare = rides.aggregate(avg=Avg("fare"))["avg"] or 0

        # Payment breakdown (by method)
        breakdown = (
            rides.values("payment_method")
            .annotate(count=Count("id"))
            .order_by()
        )
        payment_breakdown = {item["payment_method"]: item["count"] for item in breakdown}

        # Build serializer instance
        data = {
            "total_rides": total_rides,
            "total_earnings": total_earnings,
            "payment_breakdown": payment_breakdown,
            "average_fare": average_fare,
        }
        return cls(data).data
