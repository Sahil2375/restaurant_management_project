from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from orders.models import Order, OrderItem
from home.models import MenuItem

# Create your tests here.

class OrderModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser")
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.order = Order.objects.create(
        customer_name="Test User",
        user=self.user  # Provide the required user
    )

        self.order = Order.objects.create(customer_name="Test User")
        self.pizza = MenuItem.objects.create(name="Pizza", price=Decimal("10.00"))
        self.burger = MenuItem.objects.create(name="Burger", price=Decimal("5.00"))

        OrderItem.objects.create(order=self.order, menu_item=self.pizza, quantity=2, price=self.pizza.price)
        OrderItem.objects.create(order=self.order, menu_item=self.burger, quantity=1, price=self.burger.price)

        Order.objects.create(user=user, status='Completed', total_amount=100)
        Order.objects.create(user=user, status='Completed', total_amount=150)
        Order.objects.create(user=user, status='Pending', total_amount=200)


    def test_calculate_total(self):
        total = self.order.calculate_total()
        expected_total = (Decimal("10.00") * 2) + (Decimal("5.00") * 1)  # 20 + 5 = 25
        self.assertEqual(total, expected_total)

    def test_calculate_total_revenue(self):
        total_revenue = Order.calculate_total_revenue()
        self.assertEqual(total_revenue, 250)  # Only Completed orders counted