from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', signin, name='signin'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('home/', home, name='home'),
    path('profilepage/', profilepage, name='profilepage'),
    path('editprofile/', editprofile, name='editprofile'),
    path('createPost/', createPost, name='createPost'),
    path('comments/', comments, name='comments'),
    path('addFood/', addFood, name='addFood'),
    path('viewFood/', viewFood, name='viewFood'),
    path('deleteFood/<int:id>/', deleteFood, name='deleteFood'),
    path('editFood/<int:id>/', editFood, name='editFood'),

    path('viewConsumedCalories/', viewConsumedCalories, name='viewConsumedCalories'),
    path('addConsumedCalories/', addConsumedCalories, name='addConsumedCalories'),
    path('addFoodsCalories/<int:id>/', addFoodsCalories, name='addFoodsCalories'),
    path('addRestFoodsCalories/<int:id>/', addRestFoodsCalories, name='addRestFoodsCalories'),
    path('deleteConsumedCalories/<int:id>/', deleteConsumedCalories, name='deleteConsumedCalories'),

    path('postSection/', postSection, name='postSection'),
    path('friendlist/', friendlist, name='friendlist'),
    path('veiwFriendsProfile/<int:id>', veiwFriendsProfile, name='veiwFriendsProfile'),
    path('Follow/<int:id>', Follow, name='Follow'),
    path('unFollow/<int:id>', unFollow, name='unFollow'),
    path('followerlist/', followerlist, name='followerlist'),   
    path('deleteFollower/<str:userid>', deleteFollower, name='deleteFollower'),
    path('viewrestaurantfood/<str:id>', viewrestaurantfood, name='viewrestaurantfood'),
    path('followinglist/', followinglist, name='followinglist'),
    path('friendFollower/<str:id>', friendFollower, name='friendFollower'),
    path('friendFollowing/<str:id>', friendFollowing, name='friendFollowing'),


    path('restaurantListPage/', restaurantListPage, name='restaurantListPage'),
    path('gymPage/', gymPage, name='gymPage'),
    path('exercisePage/', exercisePage, name='exercisePage'),
    path('restOrSleepPage/', restOrSleepPage, name='restOrSleepPage'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
