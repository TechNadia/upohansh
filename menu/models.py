from django.db import models
from category.models import Category
from django.contrib.auth.models import User 
# Create your models here.

class FoodItem (models.Model):
    food_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    food_price = models.IntegerField()
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    food_image = models.ImageField(upload_to='photos/foods', blank=True) 
    #is it mandatory to say null=True when I am saying blank=True
    food_description = models.TextField(max_length=500, blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.food_name} {self.food_price}'


class Review(models.Model):
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')])
    comment = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.food.food_name} {self.user.username} {self.rating}'
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    estimated_delivery_time = models.PositiveIntegerField()  # Estimated delivery time in minutes

