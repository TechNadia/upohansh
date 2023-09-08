from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordChangeView
from .forms import CustomPasswordChangeForm
from cart.models import Cart, CartItem
from orders.models import Order, OrderFoodItem

# Create your views here.
def trace_order(request):    
    return render(request, 'accounts/trace_order.html')

def change_password(request):
    return (request, 'accounts/change_password.html')

def password_change_done(request):
    return render(request, 'accounts/password_change_done.html')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'  # Create a template for the password change form
    form_class = CustomPasswordChangeForm
    success_url = 'password_change_done/'  # Redirect to a success page after password change
    #return redirect('success_url')


def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_item = OrderFoodItem.objects.filter(user=request.user).order_by('-created_at')
    #print(orders)
    return render(request, 'accounts/profile.html', {'orders': orders, 'items':order_item})

def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    try:
        order_item = OrderFoodItem.objects.filter(user=request.user, order =  order)        
    except:
        order_item=None
    #print(order_item)
    return render(request, 'accounts/order_details.html', {'order':order, 'items':order_item})

def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_item = OrderFoodItem.objects.filter(user=request.user).order_by('-created_at')
    #print(orders)
    return render(request, 'accounts/order_history.html', {'orders': orders, 'items':order_item})

def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def user_signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        session_id = get_create_session(request)
        print('session_id:', session_id)
        login(request, user)
        
        
        cart = Cart.objects.filter(cart_id=session_id).first()
        is_cart_item_exists = CartItem.objects.filter(cart=cart).exists
        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(cart = cart)
            for item in cart_items:
                if item.user == user:
                    item.quantity+=1
                else:   
                    item.user = user
                item.save()
        #login(request, user)
        return redirect('menu')
    return render(request, 'accounts/signin.html')

def user_signout(request):
    print("signout:")
    logout(request)
    return render(request, 'index.html')

def signup(request):
    form = RegistrationForm()
    if request.method == "POST":
        print("signup")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("signup")
            print(form.cleaned_data.get('first_name'))
            user = form.save()
            login(request, user)
            return redirect('menu')
        else:
            print(form.errors)
    return render(request, 'accounts/register.html', {'form': form})
