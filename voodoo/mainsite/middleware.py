from voodoo.mainsite.basket.cart import Cart


class BasketMiddlWare(object):
    def process_request(self, request):
        cart = Cart(request)
        request.basket_number = len(cart.cart.orderitem_set.all())
