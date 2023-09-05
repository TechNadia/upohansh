from django.contrib import admin
from .models import FoodItem, Review

# Register your models here.
class StoreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_name', )}
    list_display = ('food_name', 'slug', 'food_price', 'is_available', 'category', 'modified_date')
    
admin.site.register(FoodItem, StoreAdmin)
admin.site.register(Review)