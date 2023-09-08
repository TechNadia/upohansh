from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
from .forms import OrderForm
from decimal import Decimal

from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
from .forms import OrderForm
from .ssl import sslcommerz_payment_gateway
from .models import Payment, OrderFoodItem, Order
from menu.models import FoodItem
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch') # csrf ke disable kore deoya
def success_view(request):
    data = request.POST
    print('data -------', data)
    user_id = int(data['value_b'])  # Retrieve the stored user ID as an integer
    user = User.objects.get(pk=user_id)
    print("user: ", user)
    print("type(data['value_a']): ", type(data['value_a']))
    payment = Payment(
        user = user,
        payment_id =data['tran_id'],
        payment_method = data['card_issuer'],
        amount_paid = int(data['store_amount'][0]),
        status =data['status'],
    )
    payment.save()
    
    # working with order model
    order = Order.objects.get(user=user, is_ordered=False, order_number=data['value_a'])
    order.payment = payment
    order.is_ordered = True
    order.save()
    cart_items = CartItem.objects.filter(user = user)
    
    for item in cart_items:
        order_item = OrderFoodItem()
        food = FoodItem.objects.get(id=item.food_item.id)
        order_item.order = order
        order_item.payment = payment
        order_item.user = user
        order_item.food = food
        order_item.quantity = item.quantity
        order_item.ordered = True
        order_item.save()

        # Reduce the quantity of the sold products
        
        food.save()

    # Clear cart
    CartItem.objects.filter(user=user).delete()
    return redirect('cart')
    
def complete(request):
    return render(request, 'orders/complete.html')

def place_order(request):
    print("Going to place an order:")
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    
    if request.user.is_authenticated :
        cart_items = CartItem.objects.filter(user = request.user)
        if cart_items.count()>0:
            for item in cart_items:
                total += item.sub_total()
            """tax += total*.05
            grand_total = total+tax"""
            tax += Decimal(.05)*total
            grand_total = total+tax
            print("cart_items: ", list(cart_items))
        else:
            return redirect('menu')
        
        if request.method=='POST':
            form = OrderForm(request.POST)
            print("request method: ", request.method)
            if form.is_valid():
                print("request method: ", request.method)
                form.instance.user = request.user
                form.instance.order_total = grand_total
                form.instance.tax = tax
                form.instance.ip = request.META.get('REMOTE_ADDR')
                #form.instance.payment = 2
                saved_instance = form.save()
                form.instance.order_number = saved_instance.id
                print("type(saved_instance.id): ", type(saved_instance.id))
                print("request.user.id: ", request.user.id)
                form.save()
                print(form)
                return redirect(sslcommerz_payment_gateway(request,  saved_instance.id, request.user.id, round(grand_total, 2)))
            else:
                print(form.errors)
    
    return render(request, 'orders/place_order.html', {'cart_items': cart_items, 'total':total, 'tax':round(tax, 2), 'grand_total':round(grand_total, 2)})

def checkout(request):
    return (request, '')


"""def checkout(request):
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
    
    return render(request, 'orders/place_order.html', {'cart_items': cart_items, 'total':total, 'tax':round(tax, 2), 'grand_total':grand_total})
"""
