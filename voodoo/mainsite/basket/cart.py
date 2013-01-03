#coding=utf-8

import datetime
from voodoo.admin_center.models import OrderItem
import models

CART_ID = 'CART-ID'


class ItemAlreadyExists(Exception):
    print "Item already exist"


class ItemDoesNotExist(Exception):
    print "Item does not exist"


class Cart:
    def __init__(self, request):
        cart_id = request.session.get(CART_ID)
        if cart_id:
            try:
                cart = models.Cart.objects.get(id=cart_id, checked_out=False)
            except models.Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.orderitem_set.all():
            yield item

    def syncPrices(self):
        for item in self:
            item.unit_price = item.product.price
            item.save()

    def new(self, request):
        cart = models.Cart(creation_date=datetime.datetime.now())
        cart.save()
        request.session[CART_ID] = cart.id
        return cart

    def add(self, product, quantity=1):
        try:
            item = OrderItem.objects.get(
                cart=self.cart,
                product=product,
            )
        except OrderItem.DoesNotExist:
            item = OrderItem()
            item.cart = self.cart
            item.product = product
            item.code = product.code
            item.brand = product.brand
            item.price_1 = product.price
            item.price_2 = product.price
            item.supplier = product.supplier.name
            item.delivery_time = product.supplier.delivery_time
            item.count = quantity
            item.status = 'Сообщен'
            item.save()
        else:
            print "Продукт уже добавлен в корзину"
            # raise ItemAlreadyExists

    def remove(self, product):
        try:
            item = OrderItem.objects.get(
                cart=self.cart,
                product=product,
            )
        except OrderItem.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, quantity):
        try:
            item = OrderItem.objects.get(
                cart=self.cart,
                product=product,
            )
            item.price_2 = product.price
            item.count = quantity
            item.save()
        except OrderItem.DoesNotExist:
            raise ItemDoesNotExist

    def clear(self):
        for item in self:
            item.delete()

    def change_id(self, request):
        request.session[CART_ID] = -1

    def getItemCount(self):
        return len(self.cart.orderitem_set.all())

    def getTotalPrice(self):
        return sum([(item.total_price) for item in self])

    def getTotalPricesAsStrList(self):
        return [str(item.total_price) for item in self]
