from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    homepage,
    menu_list_view,
    contact_us_view,
    homepage_view,
    homepage_views,
    reservations_view,
    about_view,
    OrderHistoryView,
    OrderDetailView,
    OrderViewSet,
    UpdateOrderStatusView,
    UpdateOrderStatusAPIView,
    get_order_status,
    CouponValidationView,
    MenuCategoryListView,
    UserOrderHistoryView,
    OrderStatusUpdateView,
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = router.urls
[
    path('', homepage, name='homepage'),
    path('menu/', menu_list_view, name='menu-list'),
    path('contact/', contact_us_view, name='contact-us'),
    path('home/', homepage_view, name='home-view'),
    path('home-db/', homepage_views, name='home-db-view'),
    path('reservations/', reservations_view, name='reservations'),
    path('about/', about_view, name='about'),
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),  # New detail view
    path('orders/update-status/', UpdateOrderStatusView.as_view(), name='update-order-status'),  # New status update view
    path('api/orders/<str:short_id>/status/', UpdateOrderStatusAPIView.as_view(), name='order-status'),  # New API view
    path('api/orders/<int:order_id>/status/', get_order_status, name='get-order-status'),  # New API endpoint
    path('api/coupons/validate/', CouponValidationView.as_view(), name='validate-coupon'),
    path('api/categories/', MenuCategoryListView.as_view(), name='menu-categories'),
    path('orders/history/', UserOrderHistoryView.as_view(), name='user-order-history'),
    path('orders/<int:order_id>/update-status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
]