from django.db import models
from customers.models import Customers
from products.models import Products

# Create your models here.

class Order(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))
    
    CART_STAGE = 0
    ORDER_CONFIRMED = 1
    ORDER_PROCESSED = 2
    ORDER_DELIVERED = 3
    ORDER_REJECTED = 4

    STATUS_CHOICE = (
        (CART_STAGE, 'CART_STAGE'),
        (ORDER_CONFIRMED, 'ORDER_CONFIRMED'),
        (ORDER_PROCESSED, 'ORDER_PROCESSED'),
        (ORDER_DELIVERED, 'ORDER_DELIVERED'),
        (ORDER_REJECTED, 'ORDER_REJECTED'),
    )
    order_status = models.IntegerField(choices=STATUS_CHOICE, default=CART_STAGE)
    owner = models.ForeignKey(Customers, on_delete=models.SET_NULL, null=True, related_name='orders')
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

def __str__(self) -> str:

    return "order-{}-{}".format(self.id,self.owner.name)

class OrderedItem(models.Model):
    product = models.ForeignKey(Products, related_name='added_carts', on_delete=models.SET_NULL, null=True)
    quantity=models.IntegerField(default=1)
    owner=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='added_items')