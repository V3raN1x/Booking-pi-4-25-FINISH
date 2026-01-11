from .models import Hotel, Room
from modeltranslation.translator import TranslationOptions,register

@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('hotel_name', 'street', 'description')


@register(Room)
class RoomTranslationOptions(TranslationOptions):
    fields = ('room_type', 'room_status', 'description')
