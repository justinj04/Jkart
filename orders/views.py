# Updated `views.py`
from django.shortcuts import render, redirect
from .models import Order, OrderedItem
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

def add_to_cart(request):
    if request.method == "POST": 
        user = request.user
        try:
            customer = user.customer_profile
        except AttributeError:
            # Redirect to login if the user is not authenticated
            return redirect('login')

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
