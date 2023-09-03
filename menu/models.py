from django.db import models
from category.models import Category
# Create your models here.

class FoodItem (models.Model):
    food_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    food_price = models.IntegerField()
    food_image = models.ImageField(upload_to='photos/foods', blank=True) 
    #is it mandatory to say null=True when I am saying blank=True
    food_description = models.TextField(max_length=500, blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.food_name} {self.food_price}'

