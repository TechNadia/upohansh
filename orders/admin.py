from django.contrib import admin
from .models import Order, OrderFoodItem, Payment, PaymentGatewaySettings

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderFoodItem)
admin.site.register(Payment)
admin.site.register(PaymentGatewaySettings)
