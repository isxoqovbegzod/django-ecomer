from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import store.views


class Customer(models.Model):
    """Mijoz"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Mahsulotlar"""
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)  # raqamli
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    """Buyurtma"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    data_orderd = models.DateTimeField(auto_now_add=True)
    complate = models.BooleanField(default=False, null=True, blank=False)  # to'ldirish
    transection_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False  #yetkazip berishs


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.qunatity for item in orderitems])
        return total


class OrderItem(models.Model):
    """Buyurtma elementi"""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    qunatity = models.IntegerField(default=0, null=True, blank=True)  # miqdori
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.qunatity
        return total


class ShippingAddress(models.Model):
    """Yetkazish manzili"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=255, null=True)
    date_added = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.address
