from django.urls import path, include
from django.contrib import admin
from django.shortcuts import render
from rest_framework.routers import DefaultRouter
from . import views
from .views import RiderRegisterView, DriverRegisterView, MenuCategoryViewSet, MenuCategoryListAPIView, MenuItemViewSet, MenuItemsByCategoryView, ContactFormSubmissionView, DailySpecialListView, CreateReviewView, MenuItemReviewsView, UpdateMenuItemAvailability, RestaurantInfoView, AvailableTablesAPIView, TableDetailAPIView, search_menu_items, OpeningHourListView

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet, basename='menuitem')
router.register(r'menu-categories', MenuCategoryViewSet, basename='menu-category')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

urlpatterns = [
    path('', include(router.urls)),
    path("menu-items-by-category/", MenuItemsByCategoryView.as_view(), name="menu-items-by-category"),
    path('', views.homepage, name='homepage1'),
    path('reservations/', views.reservations, name='reseravtions'),
    path('our_story/', views.our_story_view, name='our_story'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu_view, name='menu'),
    path("gallery/", views.gallery, name="gallery"),
    path("api/rider/register/", RiderRegisterView.as_view(), name="rider-register"),
    path("api/driver/register/", DriverRegisterView.as_view(), name="driver-register"),
    path("api/menu-categories/", MenuCategoryListAPIView.as_view(), name="menu-categories-list"),
    path("api/contact/", ContactFormSubmissionView.as_view(), name="contact-form"),
    path("api/daily-specials/", DailySpecialListView.as_view(), name="daily-specials"),
    path("api/reviews/create", CreateReviewView.as_view(), name="create-review"),
    path("api/reviews/menu-item/<int:menu_item_id>/", MenuItemReviewsView.as_view(), name='menu-item-reviews'),
    path("api/menu-items/<int:pk>/availability/", UpdateMenuItemAvailability.as_view(), name="update-menu-item-availability"),
    path("api/restaurant/info/", RestaurantInfoView.as_view(), name="restaurant-info"),
    path("api/tables/available/", AvailableTablesAPIView.as_view(), name="available_tables_api"),
    path("api/tables/<int:pk>/", TableDetailAPIView.as_view(), name="table-detail-api"),
    path("api/menu/search/", search_menu_items, name="menu-search"),
    path("restaurant/opening-hours/", OpeningHourListView.as_view(), name="opening-hours"),
]

handler404 = 'home.urls.custom_404_view'