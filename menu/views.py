from django.shortcuts import render, get_object_or_404
from .models import FoodItem
from category.models import Category
# Create your views here.
def menu(request, category_slug = None):
    category = None
    foods = None
    if category_slug!=None:
        category = get_object_or_404(Category, slug = category_slug)
        foods = FoodItem.objects.filter(is_available = True, category = category)
    else:
        foods = FoodItem.objects.all()
    
    categories = Category.objects.all()
    #print(foods)
    context = {'food_item': foods, 'categories': categories}
    return render(request, 'food_menu.html', context)

