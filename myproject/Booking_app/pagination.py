from rest_framework import generics
from rest_framework.pagination import PageNumberPagination



class HotelListAPIView(generics.ListAPIView):
    page_size = 5

class RoomPagination(PageNumberPagination):
    page_size = 8
