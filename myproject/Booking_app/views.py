from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, City, Service, Hotel, HotelImage, Room, RoomImage, Review, Booking
from .serializers import (UserProfileListSerializer, UserProfileDetailSerializer, CityListSerializer, CityDetailSerializer, ServiceSerializer,
                          HotelListSerializer, HotelDetailSerializer, HotelImageSerializer, RoomListSerializer,
                          RoomDetailSerializer, RoomImageSerializer, ReviewCreateSerializer, BookingSerializer,
                          HotelCreateSerializer, UserRegisterSerializer, UserLoginSerializer)
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import HotelFilter, RoomFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import CheckRolePermissions, CreateHotelPermissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView



class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class CityListAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializer

class CityDetailAPIView(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class HotelListAPIView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HotelFilter
    search_fields = ['hotel_name',]
    ordering_fields = ['hotel_starts']

class HotelDetailAPIView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializer

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelCreateSerializer
    permission_classes = CreateHotelPermissions

    def get_queryset(self):
        return Hotel.objects.filter(owner=self.request.user)


class HotelImageViewSet(viewsets.ModelViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer

class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer

class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RoomFilter
    search_fields = ['room_type, room_status, price',]
    ordering_fields = ['price']

class RoomImageViewSet(viewsets.ModelViewSet):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [CheckRolePermissions]

class ReviewEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [CheckRolePermissions]

    def get_queryset(self):
        return Review.objects.filter()

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [CheckRolePermissions]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)