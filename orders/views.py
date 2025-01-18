from django.shortcuts import render,redirect
from .models import Order,OrderedItem
from products.models import Products

# Create your views here.

def show_cart(request):
    user=request.user
    customer=user.customer_profile
    cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
    context={'cart':cart_obj}

    return render(request,'cart.html')

def add_to_cart(request):
    if request.POST:
        user=request.user
        customer=user.customer_profile
        quantity=request.POST.get('quantity')
        product_id=request.POST.get('product_id')
        cart_obj, created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        try:
            product=Products.objects.get(pk=product_id)
            ordered_item=OrderedItem.objects.create(
                product=product,
                owner=cart_obj,
                quantity=quantity
            )
        except Products.DoesNotExist:    
            return redirect('cart')