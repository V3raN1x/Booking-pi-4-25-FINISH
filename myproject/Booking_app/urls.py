from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CityListAPIView, CityDetailAPIView,
                    ServiceViewSet, HotelImageViewSet,
                    RoomListAPIView, RoomDetailAPIView,
                    RoomImageViewSet, ReviewCreateAPIView,
                    ReviewEditAPIView, BookingViewSet,
                    HotelListAPIView, HotelDetailAPIView,
                    UserProfileListAPIView, UserProfileDetailAPIView,
                    HotelViewSet, RegisterView,
                    LoginView, LogoutView
                    )

router = DefaultRouter()
router.register(r'service', ServiceViewSet),
router.register(r'hotelImage', HotelImageViewSet),
router.register(r'roomImage', RoomImageViewSet),
router.register(r'booking', BookingViewSet)
router.register(r'hotel_create', HotelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('hotel/', HotelListAPIView.as_view(), name='hotel_list'),
    path('hotel/<int:pk>/', HotelDetailAPIView.as_view(), name='hotel_detail'),
    path('city/', CityListAPIView.as_view(), name='city_list'),
    path('city/<int:pk>/', CityDetailAPIView.as_view(), name='city_detail'),
    path('rooms/', RoomListAPIView.as_view(), name='room_list'),
    path('rooms/<int:pk>/', RoomDetailAPIView.as_view(), name='room_detail'),
    path('users/', UserProfileListAPIView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('reviews/', ReviewCreateAPIView.as_view(), name='create_review'),
    path('reviews/<int:pk>/', ReviewEditAPIView.as_view(), name='edit_review'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]