from django.contrib import admin
from .models import (
    Country, UserProfile, City, Service,
    Hotel, HotelImage, Room, RoomImage,
    Review, Booking
)
from modeltranslation.admin import TranslationAdmin

@admin.register(Hotel, Room)
class ProductAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(Country)
admin.site.register(UserProfile)
admin.site.register(City)
admin.site.register(Service)
admin.site.register(HotelImage)
admin.site.register(RoomImage)
admin.site.register(Review)
admin.site.register(Booking)
