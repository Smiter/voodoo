#coding=utf-8

from cart import Cart
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import *
from models import Product
from voodoo.mainsite.views import DjangoJSONEncoder
from voodoo.mainsite.models import Order, MyRegistrationProfile
from django.utils.simplejson import dumps
# from voodoo.mainsite.basket.models import Product


def add_to_cart(request):
    print "add to cart\n"
    print request.POST["item_id"]
    product = Product.objects.get(id=request.POST["item_id"])
    cart = Cart(request)
    cart.add(product)
    request.basket_number = len(cart.cart.item_set.all())
    total_price = sum([(item.total_price) for item in cart.cart.item_set.all()])
    return render_to_response('basket.html',  dict(cart=cart, total_price=total_price, products=Product.objects.all()), context_instance=RequestContext(request))


def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)


def get_basket(request):
    cart = Cart(request)
    total_price = sum([(item.total_price) for item in cart.cart.item_set.all()])
    return render_to_response('basket.html',  dict(cart=cart, products=Product.objects.all(), total_price=total_price), context_instance=RequestContext(request))


def update_basket(request):
    for product_id, quantity in request.POST.iteritems():
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.update(product, quantity)
    output = [str(item.total_price) for item in cart.cart.item_set.all()]
    return HttpResponse(dumps(output), mimetype="application/json")


def del_item(request):
    product = Product.objects.get(id=request.POST["id"])
    cart = Cart(request)
    cart.remove(product)
    output = [str(item.total_price) for item in cart.cart.item_set.all()]
    return HttpResponse(dumps(output), mimetype="application/json")


def make_order(request):
    cart = Cart(request)
    user = request.user
    if not user.is_authenticated():
        print "SDsdadas"
        user = MyRegistrationProfile.objects.create_inactive_user(
            request.POST["name"], "sda@da.com", "232323", "sda", False)

    order = Order(user=user, status=u'Сообщён')
    order.save()
    for item in cart.cart.item_set.all():
        order.items.add(item)

    cart.change_id(request)
    cart = Cart(request)
    request.basket_number = len(cart.cart.item_set.all())
    return render_to_response('basket.html',  dict(cart=cart, products=Product.objects.all(), total_price=0), context_instance=RequestContext(request))
    