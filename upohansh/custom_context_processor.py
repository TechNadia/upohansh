# yourapp/context_processors/cart_context_processor.py
from cart.models import CartItem, Cart

def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key
    
    
def cart_context(request):
    food_quantity = 0
    if request.user.is_authenticated:
        cart_exists = CartItem.objects.filter(user = request.user).exists()
        if cart_exists: 
            foods = CartItem.objects.filter(user = request.user)
            #print("food count: ", foods)
            for food in foods:
                food_quantity += food.quantity
      
    else:  
        session_id = get_create_session(request)
        #print('within cart: session_id-', session_id)
        cart = Cart.objects.filter(cart_id = session_id).first()
        cart_exists = CartItem.objects.filter(cart=cart).exists()
        #print("cart exists: ", cart_exists)
        if cart_exists: 
            foods = CartItem.objects.filter(cart=cart)
            print("food count: ", foods)
            for food in foods:
                food_quantity += food.quantity
            
    #print("Total Quantity: ", food_quantity)
    request.session['food_quantity'] = food_quantity
    return {}
