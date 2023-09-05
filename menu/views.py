from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem, Review, Location
from category.models import Category
from .forms import ReviewForm
# Create your views here.

def specials(request):
    discounted_food_item = FoodItem.objects.filter(discount_price__isnull=False)
    return render(request, 'food_menu.html', {'food_item': discounted_food_item})

def estimate_delivery(request, location_id):
    location = Location.objects.get(pk=location_id)
    return render(request, '', {'location': location})


def food_detail(request, food_id):
    food_item = None
    reviews = None
    form = None
    food_item = FoodItem.objects.get(id=food_id)
    print(request.method)
    if food_item:
        reviews = Review.objects.filter(food=food_item).order_by('-date_time')
        print(reviews)
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            #print(form.cleaned_data)
            if form.is_valid():
                review = form.save(commit=False)
                review.food = food_item
                review.user = request.user
                review.save()
                #return redirect('detail')
            else:
                print("Getting error: ", form.errors)

        else:
            form = ReviewForm()
    return render(request, 'food_detail.html', {'food_item':food_item, 'reviews': reviews, 'form': form})

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

