from django.contrib import admin
from .models import Dealer, Review, CarMake, CarModel

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "state")
    list_filter = ("state",)
    search_fields = ("name", "city", "state")
    inlines = [ReviewInline]

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

admin.site.register(Review)
admin.site.register(CarModel)
