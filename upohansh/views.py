from django.shortcuts import render
from menu.models import FoodItem

# Create your views here.
def home(request):
    food_items = FoodItem.objects.all()
    return render(request, 'index.html', {"food":food_items})
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')