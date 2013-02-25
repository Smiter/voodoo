#coding=utf-8

from cart import Cart
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import *
from voodoo.admin_center.models import Product
from voodoo.admin_center.models import Order, OrderStatus
from django.utils.simplejson import dumps


def add_to_cart(request):
    print "add to cart\n"
    product = Product.objects.get(id=request.POST["product_id"])
    cart = Cart(request)
    cart.add(product)
    request.basket_number = cart.getItemCount()
    return render_to_response('basket.html',  dict(cart=cart, total_price=cart.getTotalPrice(), products=Product.objects.all()), context_instance=RequestContext(request))


def get_basket(request):
    cart = Cart(request)
    return render_to_response('basket.html',  dict(cart=cart, products=Product.objects.all(), total_price=cart.getTotalPrice()), context_instance=RequestContext(request))


def update_basket(request):
    for item_id, quantity in request.POST.iteritems():
        cart = Cart(request)
        cart.update(item_id, quantity)
        result = {
        'prices': cart.getTotalPricesAsStrList(),
        'total_price': cart.getTotalPrice()
        }
    return HttpResponse(dumps(result), mimetype="application/json")


def del_item(request):
    cart = Cart(request)
    cart.remove(request.POST["id"])
    return HttpResponse(dumps(cart.getTotalPricesAsStrList()), mimetype="application/json")


def make_order(request):
    cart = Cart(request)
    user = request.user
    order = None
    if not user.is_authenticated():
        order = Order(client_name=u'Не зарегистрирован, ' + request.POST["name"], client_phone=request.POST["phone"], order_status=OrderStatus.objects.get(status='Принят'))
        order.order_info = "\n".join([item.product.brand + " " + str(item.count) for item in cart])
        order.save()
        for item in cart:
            item.order = order
            item.code = item.product.code
            item.brand = item.product.brand
            item.price_1 = item.product.price_with_currency
            item.price_2 = item.get_price_with_discount()
            item.supplier = item.product.supplier
            item.save()
    else:
        for item in cart:
            item.user = user
            item.code = item.product.code
            item.brand = item.product.brand
            item.price_1 = item.product.price_with_currency
            item.price_2 = item.get_price_with_discount()
            item.supplier = item.product.supplier
            item.save()
    cart.cart.checked_out = True
    cart.cart.save()
    cart.change_id(request)
    cart = Cart(request)
    request.basket_number = 0
    return HttpResponseRedirect("/basket")
