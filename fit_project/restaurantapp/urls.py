from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('restaurant_signup/', restaurant_signup, name='restaurant_signup'),
    path('restaurant_login/', restaurant_login, name='restaurant_login'),
    path('restaurant_signout/', restaurant_signout, name='restaurant_signout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', homePage, name='homePage'),
    path('aboutPage/', aboutPage, name='aboutPage'),
    path('servicePage/', servicePage, name='servicePage'),
    path('contactPage/', contactPage, name='contactPage'),
    path('afterLoginDashboard/', afterLoginDashboard, name='afterLoginDashboard'),
    path('restaurantForm/', restaurantForm, name='restaurantForm'),
    path('viewRestaurantFood/<str:id>', viewRestaurantFood, name='viewRestaurantFood'),
    path('editRestaurantFood/<str:id>', editRestaurantFood, name='editRestaurantFood'),
    path('updateRestaurantFood/', updateRestaurantFood, name='updateRestaurantFood'),
    path('deleteRestaurantFood/<str:id>', deleteRestaurantFood, name='deleteRestaurantFood'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)