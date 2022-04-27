from django.shortcuts import render
from . import models
from django.shortcuts import render
from django.http import JsonResponse
import json


# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = models.Order.objects.get_or_create(customer=customer, complate=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0}
        cartItems = order['get_cart_item']

    items = models.Product.objects.all()
    context = {'items': items, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    # global order
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = models.Order.objects.get_or_create(customer=customer, complate=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0}
        cartItems = order['get_cart_item']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = models.Order.objects.get_or_create(customer=customer, complate=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(action, '_______________________________')
    print(productId, 'product ________________')

    customer = request.user.customer
    product = models.Product.objects.get(id=productId)
    order, created = models.Order.objects.get_or_create(customer=customer, complate=False)
    orderItem, created = models.OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.qunatity = (orderItem.qunatity + 1)
        print("adddddddddddddddddd")
    elif action == 'remove':
        orderItem.qunatity = (orderItem.qunatity - 1)
    orderItem.save()

    if orderItem.qunatity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)
