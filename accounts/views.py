from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from cart.models import Cart, CartItem

# Create your views here.

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
        login(request, user)
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
