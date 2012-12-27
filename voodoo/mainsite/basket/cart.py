#coding=utf-8

import datetime
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
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            item.unit_price = product.price
            item.quantity = quantity
            item.save()
        else:
            raise ItemAlreadyExists

    def remove(self, product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, quantity):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
            item.unit_price = product.price
            item.quantity = quantity
            item.save()
        except models.Item.DoesNotExist:
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
