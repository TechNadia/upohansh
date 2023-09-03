from django.shortcuts import render, redirect
from menu.models import FoodItem
from .models import Cart, CartItem

# Create your views here.
def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key
    
def cart(request):
    session_id = get_create_session(request)
    print('session_id:', session_id)
    cart_id = Cart.objects.filter(cart_id = session_id).exists()
    print('cart_id:', cart_id)
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    
    if not request.user.is_authenticated and cart_id:
        cart_obj = Cart.objects.get(cart_id = session_id)
        #cart_obj_filter = Cart.objects.filter(cart_id = session_id)
        print("cart_obj: ", type(cart_obj))
        #print("cart_obj_filter: ", type(cart_obj_filter))
        cart_items = CartItem.objects.filter(cart = cart_obj)        
    elif request.user.is_authenticated :
        cart_items = CartItem.objects.filter(user = request.user)
    elif not request.user.is_authenticated and not cart_id:
        cart_items=None
    if cart_items:
        for item in cart_items:
            total += item.sub_total()
        tax += total*.05
        grand_total = total+tax
        print("cart_items: ", list(cart_items))
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total':total, 'tax':tax, 'grand_total':grand_total})
    #return render(request, 'cart/cart.html')


def add_to_cart(request, food_id):
    print("food_id: ", food_id)    
    food = FoodItem.objects.get(id=food_id)
    print("selected food: ", food)
    session_id = get_create_session(request)
    
    if request.user.is_authenticated:
        print("user exists")
        cart_item = CartItem.objects.filter(food_item = food, user = request.user).exists()
        print("cart_item: ", cart_item)
        if cart_item:
            item = CartItem.objects.get(food_item = food)
            item.quantity+=1            
            item.save()
        else:
            print("session_id: ", session_id)
            try:
                cart = Cart.objects.get(cart_id=session_id)
            except Cart.DoesNotExist:
                # Handle the case where the cart doesn't exist, e.g., create a new cart
                cart = Cart.objects.create(cart_id=session_id)
                cart.save()

            print("cart: ", cart)
            cart_item = CartItem.objects.create(food_item = food, quantity = 1, cart = cart, user = request.user)
            cart_item.save()
    else:        
        cart_id = Cart.objects.filter(cart_id = session_id).exists()
        print("cart_id: ", cart_id)
        if cart_id:   
            cart_item = CartItem.objects.filter(food_item = food).exists()
            print("cart_item: ", cart_item)
            if cart_item:
                item = CartItem.objects.get(food_item = food)
                item.quantity+=1            
                item.save()
            else:
                print("session_id: ", session_id)
                cart = Cart.objects.get(cart_id = session_id)
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
            cart_item = CartItem.objects.get(food_item = food)
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


def checkout(request):
    print("Checkout: ", request.POST)
    session_id = get_create_session(request)
    print('session_id:', session_id)
    cart_id = Cart.objects.filter(cart_id = session_id).exists()
    print('cart_id:', cart_id)
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    
    if request.user.is_authenticated :
        cart_items = CartItem.objects.filter(user = request.user)
    else:
        return redirect('signin')
    if cart_items:
        for item in cart_items:
            total += item.sub_total()
        tax += total*.05
        grand_total = total+tax
        print("cart_items: ", list(cart_items))
    #return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total':total, 'tax':tax, 'grand_total':grand_total})
    
    return render(request, 'cart/place_order.html', {'cart_items': cart_items, 'total':total, 'tax':tax, 'grand_total':grand_total})

