# Updated `views.py`
from django.shortcuts import render, redirect
from .models import Order, OrderedItem
from django.contrib import messages
from products.models import Products

# Show Cart
def show_cart(request):
    user = request.user
    customer = user.customer_profile
    cart_obj, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
    )
    subtotal = sum(item.product.price * item.quantity for item in cart_obj.added_items.all())
    context = {'cart': cart_obj, 'subtotal': subtotal}

    return render(request, 'cart.html', context)

def remove_item(request,pk):
    item=OrderedItem.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect('cart')    

def checkout_cart(request):
    if request.POST: 
        try:
            user = request.user
            customer = user.customer_profile
            total = float(request.POST.get('total'))
            order_obj = Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            )    
            if order_obj:
                order_obj.order_status=Order.ORDER_CONFIRMED
                order_obj.save()
                status_message="Your order is processed. your items will be devivered within 2 days."
                messages.success(request,status_message)
            else:
               status_message="unable to processed. No items in cart"
               messages.error(request,status_message) 
        except Exception as e:
               status_message="unable to processed. No items in cart"
               messages.error(request,status_message) 
    return redirect('cart')       
            
def add_to_cart(request):
    if request.method == "POST": 
        user = request.user
        try:
            customer = user.customer_profile
        except AttributeError:
            return redirect('account')

        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        try:
            product = Products.objects.get(pk=product_id)
            ordered_item,created=OrderedItem.objects.get_or_create(
                product=product,
                owner=cart_obj,
                quantity=quantity
            )
            if created:
                ordered_item.quantity=quantity
                ordered_item.save()
            else:
                ordered_item.quantity=ordered_item.quantity+quantity
                ordered_item.save()  
                  
        except Products.DoesNotExist:
            return redirect('cart')  # If product doesn't exist, go to cart

        return redirect('cart')  # Redirect to the cart after adding the item

    # Handle GET requests explicitly
    return redirect('cart')  # Redirect GET requests to the cart
