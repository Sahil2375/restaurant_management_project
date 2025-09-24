from django.test import TestCase
from decimal import Decimal
from orders.models import Order, OrderItem
from home.models import MenuItem

# Create your tests here.

class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(customer_name="Test User")
        self.pizza = MenuItem.objects.create(name="Pizza", price=Decimal("10.00"))
        self.burger = MenuItem.objects.create(name="Burger", price=Decimal("5.00"))

        OrderItem.objects.create(order=self.order, menu_item=self.pizza, quantity=2, price=self.pizza.price)
        OrderItem.objects.create(order=self.order, menu_item=self.burger, quantity=1, price=self.burger.price)

    def test_calculate_total(self):
        total = self.order.calculate_total()
        expected_total = (Decimal("10.00") * 2) + (Decimal("5.00") * 1)  # 20 + 5 = 25
        self.assertEqual(total, expected_total)