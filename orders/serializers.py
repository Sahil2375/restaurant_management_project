from rest_framework import serializers
from .models import Order, OrderItem
from home.models import MenuItem

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source="menu_item.name", read_only=True)
    price = serializers.DecimalField(source="menu_item.price", max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["menu_item_name", "quantity", "price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "total_price", "items"]

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
    order_id = serializers.CharField()
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)