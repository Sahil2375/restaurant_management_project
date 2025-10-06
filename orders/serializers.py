from rest_framework import serializers
from .models import Order, OrderItem, MenuCategory
from home.models import MenuItem

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source="menu_item.name", read_only=True)
    # price = serializers.DecimalField(source="menu_item.price", max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["menu_item_name", "quantity"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='order_items', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "status", "total_price", "items"]

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "price", "description"]

class OrderSerializer(serializers.ModelSerializer):
    # order_items = MenuItemSerializer(many=True, read_only=True)
    # user = serializers.StringRelatedField() # or 'UserSerializer' if want details

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'status', 'created_at']

class UpdateOrderStatusSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)

from rest_framework import serializers
from .models import Order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['short_id', 'status']

    def validate_status(self, value):
        allowed_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in allowed_statuses:
            raise serializers.ValidationError(f"Status must be one of {allowed_statuses}.")
        return value
    

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['id', 'name']   # include only name (id optional)
