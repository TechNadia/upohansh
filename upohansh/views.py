from django.shortcuts import render
from menu.models import FoodItem
from django.db.models import Q
from cart.models import Cart, CartItem

# Create your views here.
def home(request):
    
    food_items = FoodItem.objects.all()
    discounted_food_item = FoodItem.objects.filter(discount_price__isnull=False)
    return render(request, 'index.html', {"food":food_items, 'discounts': discounted_food_item})
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def food_search(request):
    #print("search button clicked!")
    query = request.GET.get('q')
    print(query)
    if query:
        results = FoodItem.objects.filter(
            Q(food_name__icontains=query) | Q(food_description__icontains=query)
        )
    else:
        results = FoodItem.objects.none()  # No results if no query provided
    #print(results)
    return render(request, 'search.html', {'results': results, 'query': query})

