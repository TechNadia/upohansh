from django.shortcuts import render, redirect
from menu.models import FoodItem
from .models import Cart, CartItem
from decimal import Decimal

# Create your views here.
def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key
    
def cart(request):
    session_id = get_create_session(request)
    #print('within cart: session_id-', session_id)
    cart_id = Cart.objects.filter(cart_id = session_id).exists()
    #print('within cart: cart_id-', cart_id)
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    
    """
    Cases:
    1. user logged in and has cart
    2. user not logged in and has cart
    3. user logged in and has no cart
    4. user not logged in and has no cart
    """
    if not request.user.is_authenticated and cart_id:
        cart_obj = Cart.objects.get(cart_id = session_id)
        #cart_obj_filter = Cart.objects.filter(cart_id = session_id)
        print("user not logged in, but has cart: cart_obj- ", type(cart_obj))
        #print("cart_obj_filter: ", type(cart_obj_filter))
        cart_items = CartItem.objects.filter(cart = cart_obj) 
        print("cart_items:", cart_items)       
    elif request.user.is_authenticated :
        cart_obj = Cart.objects.filter(cart_id = session_id)        
        #print(cart_obj)
        
        #print("user is logged in, but may have or may not a cart: ", request.user)
        cart_items = CartItem.objects.filter(user = request.user)
        #print(cart_items)
    elif not request.user.is_authenticated and not cart_id:
        cart_items=None
    if cart_items:
        for item in cart_items:
            print("item: ", item)
            total += item.sub_total()
            """if item.food_item.discount_price:
                print("Discounted price: ", item.food_item.discount_price)
            else:
                print("Item has not no discount price")"""
        tax += Decimal(.05)*total
        grand_total = total+tax
        #print("cart_items: ", list(cart_items))
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total':total, 'tax':round(tax, 2), 'grand_total':round(grand_total, 2)})


def add_to_cart(request, food_id):
    #print("food_id: ", food_id)    
    food = FoodItem.objects.get(id=food_id)
    #print("selected food: ", food)
    session_id = get_create_session(request)
    
    if request.user.is_authenticated:
        #print("user logged in: ")
        cart_item = CartItem.objects.filter(food_item = food, user = request.user).exists()
        #print("cart_item: ", cart_item)
        if cart_item:
            #print("Food item exists beforehand")
            item = CartItem.objects.get(food_item = food)
            item.quantity+=1            
            item.save()
        else:
            #print("No food item has been added yet!")
            #print("session_id: ", session_id)
            try:
                cart = Cart.objects.get(cart_id=session_id)
            except Cart.DoesNotExist:
                # Handle the case where the cart doesn't exist, e.g., create a new cart
                cart = Cart.objects.create(cart_id=session_id)
                cart.save()

            #print("cart: ", cart)
            cart_item = CartItem.objects.create(food_item = food, quantity = 1, cart = cart, user = request.user)
            cart_item.save()
    else: 
        #print("user not logged in: ")       
        cart_id = Cart.objects.filter(cart_id = session_id).exists()
        #print("cart_id: ", cart_id)
        if cart_id:   
            cart_item = CartItem.objects.filter(food_item = food).exists()
            print("cart_item: ", cart_item)
            if cart_item:
                print("Food item exists beforehand")
                item_exists = CartItem.objects.filter(food_item = food, cart = Cart.objects.get(cart_id = session_id)).exists()
                if item_exists:                     
                    item = CartItem.objects.get(food_item = food, cart = Cart.objects.get(cart_id = session_id))
                    item.quantity+=1  
                else:
                    item = CartItem.objects.create(food_item = food, quantity = 1, cart = Cart.objects.get(cart_id = session_id))
                    #item = CartItem.objects.create(food_item = food)
                    #item.quantity+=1          
                item.save()
            else:
                print("No food item has been added yet!")
                print("session_id: ", session_id)
                try:
                    cart = Cart.objects.get(cart_id=session_id)
                except Cart.DoesNotExist:
                    # Handle the case where the cart doesn't exist, e.g., create a new cart
                    cart = Cart.objects.create(cart_id=session_id)
                    cart.save()
                print("cart: ", cart)
                cart_item = CartItem.objects.create(food_item = food, quantity = 1, cart = cart)
                cart_item.save()
        else:
            cart = Cart.objects.create(cart_id = session_id)
            cart.save()
            cart_item = CartItem.objects.create(food_item = food, quantity = 1, cart = cart)
            cart.save()
    return redirect('cart')

def remove_from_cart(request, food_id):  
    print("remove: ", food_id)
    food = FoodItem.objects.get(id=food_id)
    print("selected food: ", food)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(food_item = food, user=request.user)
        cart_item.delete()
    else:
        session_id = request.session.session_key
        cart_id = Cart.objects.filter(cart_id = session_id).exists()
        if cart_id:   
            print("session_id: ", session_id)
            cart = Cart.objects.get(cart_id = session_id)
            cart_item = CartItem.objects.get(food_item = food, cart = Cart.objects.get(cart_id = session_id))
            cart_item.delete()
            #cart.save()
        
    return redirect('cart')
    
def decrease_cart(request, food_id):
    print("food_id: ", food_id)    
    food = FoodItem.objects.get(id=food_id)
    print("selected food: ", food)
    session_id = request.session.session_key
    cart_id = Cart.objects.filter(cart_id = session_id).exists()
    print("cart_id: ", cart_id)
    if cart_id:   
        cart_item = CartItem.objects.filter(food_item = food).exists()
        print("cart_item: ", cart_item)
        if cart_item:
            item = CartItem.objects.get(food_item = food)
            if(item.quantity>1):
                item.quantity-=1
                item.save()
                return redirect('cart')
            else:
                cart = Cart.objects.get(cart_id = session_id)
                cart_item = CartItem.objects.get(food_item = food)
                cart_item.delete()
                cart.save()    
            
    return redirect('cart')

def increase_cart(request, food_id):
    print("food_id: ", food_id)    
    food = FoodItem.objects.get(id=food_id)
    print("selected food: ", food)
    session_id = request.session.session_key
    cart_id = Cart.objects.filter(cart_id = session_id).exists()
    print("cart_id: ", cart_id)
    if cart_id:   
        cart_item = CartItem.objects.filter(food_item = food).exists()
        print("cart_item: ", cart_item)
        if cart_item:
            item = CartItem.objects.get(food_item = food, cart=Cart.objects.get(cart_id = session_id))
            #if(item.quantity<stock):
            item.quantity+=1
            item.save()
            return redirect('cart')
            """else:
                cart = Cart.objects.get(cart_id = session_id)
                cart_item = CartItem.objects.get(food_item = food)
                cart_item.delete()
                cart.save()    """
            
    return redirect('cart')


