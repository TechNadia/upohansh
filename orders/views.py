from django.shortcuts import render, redirect
def complete(request):
    return render(request, 'cart/complete.html')

def place_order(request):
    return render(request, 'cart/complete.html')