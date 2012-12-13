#coding=utf-8

from cart import Cart
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import *
from models import Product
from voodoo.mainsite.views import DjangoJSONEncoder
from django.utils.simplejson import dumps
# from voodoo.mainsite.basket.models import Product


def add_to_cart(request):
    print "add to cart\n"
    print request.POST["item_id"]
    product = Product.objects.get(id=request.POST["item_id"])
    cart = Cart(request)
    cart.add(product, proDjangoJSONEncoderduct.price)
    return render_to_response('basket.html',  dict(cart=Cart(request), products=Product.objects.all()), context_instance=RequestContext(request))


def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)


def get_basket(request):
    return render_to_response('basket.html',  dict(cart=Cart(request), products=Product.objects.all()), context_instance=RequestContext(request))


def update_basket(request):
    for product_id, quantity in request.POST.iteritems():
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.update(product, quantity, product.price)
    output = [str(item.total_price) for item in cart.cart.item_set.all()]
    return HttpResponse(dumps(output), mimetype="application/json")
