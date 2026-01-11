from .models import UserProfile, City, Service, Hotel, HotelImage, Room, RoomImage, Review, Booking, Country
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'username', 'email', 'password', 'country')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']




class CountryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_image', 'country_name']




class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'user_image', 'user_role']




class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'




class UserProfileReviewSerializer(serializers.ModelSerializer):
    country = CountryProfileSerializer()

    class Meta:
        model = UserProfile
        fields = ['first_name', 'user_image', 'country']




class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'city_image']




class CityNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']




class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_image', 'service_name']




class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel_image']




class HotelListSerializer(serializers.ModelSerializer):
    city = CityNameSerializer()
    hotel_images = HotelImageSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'hotel_images', 'city', 'hotel_starts', 'description']




class HotelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'




class CityDetailSerializer(serializers.ModelSerializer):
    city_hotels = HotelListSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ['city_name', 'city_hotels']




class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'price', 'room_type', 'room_status', 'description']




class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['room_image']




class RoomDetailSerializer(serializers.ModelSerializer):
    room_photos = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['room_number', 'price', 'room_type', 'room_status', 'description', 'room_photos']




class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"




class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%d-%m-%Y %H:%M')
    user = UserProfileReviewSerializer()

    class Meta:
        model = Review
        fields = ['user', 'comment', 'created_date']




class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'




class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_images = HotelImageSerializer(many=True, read_only=True)
    country = CountrySerializer
    city = CityNameSerializer()
    hotel_service = ServiceSerializer(many=True)
    hotel_rooms = RoomListSerializer(many=True, read_only=True)
    hotel_reviews = ReviewSerializer(many=True, read_only=True)
    get_avg_raring = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()


    class Meta:
        model = Hotel
        fields = ['hotel_name', 'country', 'city', 'hotel_starts', 'street', 'postal_code',
                  'hotel_images', 'description', 'hotel_service', 'hotel_rooms', 'get_avg_raring',
                  'get_count_people', 'hotel_reviews']

    def get_get_avg_raring(self, obj):
        return obj.get_avg_raring()
    def get_count_people(self, obj):
        return obj.get_count_people()