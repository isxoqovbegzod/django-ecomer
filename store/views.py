import datetime
# from pickletools import i

from . import models
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .utils import cookieCart

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
    json = models.Order.objects.all()
    context = {'items': items, 'cartItems': cartItems, 'shipping': False, "json":json}
    return render(request, 'store/store.html', context)


def cart(request):
    # global order
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = models.Order.objects.get_or_create(customer=customer, complate=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('cart:', cart)
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}
        cartItems = order['get_cart_item']

        for i in cart:
            try:
                cartItems += cart[i]['qunatity']

                product = models.Product.objects.get(id=i)
                total = (product.price * cart[i]['qunatity'])

                order['get_cart_total'] += total
                order['get_cart_item'] += cart[i]['qunatity']

                item = {
                    "product": {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                    },
                    'quantity': cart[i]["qunatity"],
                    'get_total': total
                }
                items.append(item)
                if product.digital == False:
                    order['shipping'] = True
            except:
                pass

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = models.Order.objects.get_or_create(customer=customer, complate=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}
        cartItems = order['get_cart_item']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = models.Product.objects.get(id=productId)
    order, created = models.Order.objects.get_or_create(customer=customer, complate=False)
    orderItem, created = models.OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.qunatity = (orderItem.qunatity + 1)
    elif action == 'remove':
        orderItem.qunatity = (orderItem.qunatity - 1)
    orderItem.save()

    if orderItem.qunatity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = models.Order.objects.get_or_create(customer=customer, complate=False)
        total = float(data['form']['total'])
        order.transection_id = transaction_id

        if total == order.get_cart_total:
            order.complate = True
        order.save()

        if order.shipping == True:
            models.ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        print("User not is logged in .....")
    return JsonResponse('Payment complate!', safe=False)

def handler404(request, exception):
    context = {}
    return render(request, 'store/error404.html', context)


