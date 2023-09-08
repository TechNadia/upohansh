from django.db import models
from menu.models import FoodItem
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.cart_id}'
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        if self.food_item.discount_price:
            print("Discounted price: ", self.food_item.discount_price)
            return self.food_item.discount_price*self.quantity
        else:
            print("Item has not no discount price")
            return self.food_item.food_price*self.quantity
    
    def __str__(self) -> str:
        return f'{self.food_item} {self.quantity}' 
