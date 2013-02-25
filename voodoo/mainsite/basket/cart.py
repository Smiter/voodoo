#coding=utf-8

import datetime
from voodoo.admin_center.models import OrderItem, ItemStatus
import models
from voodoo.mainsite.models import Profile


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
        if request.user.is_authenticated():
            self.user = request.user
            
    def __iter__(self):
        for item in self.cart.orderitem_set.all():
            yield item

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
            if hasattr(self, 'user'):
                item.user = self.user
            item.cart = self.cart
            item.product = product
            item.code = product.code
            item.brand = product.brand
            item.price_1 = product.price_with_currency
            item.price_2 = item.get_price_with_discount()
            item.supplier = product.supplier
            item.count = quantity
            item.status = ItemStatus.objects.get(status=u'Сообщен')
            item.save()
        else:
            print "Продукт уже добавлен в корзину"
            # raise ItemAlreadyExists

    def remove(self, item_id):
        try:
            item = OrderItem.objects.get(
                cart=self.cart,
                id=item_id,
            )
        except OrderItem.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, item_id, quantity):
        try:
            item = OrderItem.objects.get(
                cart=self.cart,
                id=item_id,
            )
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
        return int(sum([(item.total_price) for item in self]))

    def getTotalPricesAsStrList(self):
        return [str(item.total_price) for item in self]
