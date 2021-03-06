from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import re

# authentication is done using django auth pls add you username and passwor din admin/route Users before continuing
# add user requests to your body of the request
from products.models import Products
import json
import ast


# Create your views here.
def index(req):
    res = json.dumps([{}])
    return HttpResponse(res, content_type='text/json')


@csrf_exempt
def get_product(req):
    body_unicode = req.body.decode('utf-8')
    payload = ast.literal_eval(body_unicode)[0]
    print(payload)
    user = payload['username']
    password = payload['password']
    usr = authenticate(username=user, password=password)
    if req.method == 'GET' and usr!=None:
        id = req.GET.get('id')
        try:
            pro = list(Products.objects.filter(id=id).values())[0]
            res = json.dumps([{'message': 'product found!!!', 'sku_name': pro['sku_name'],
                               'sku_category': pro['sku_category'], 'price': pro['price']}])
        except:
            res = json.dumps([{'message': 'product does not exist'}])
        return HttpResponse(res, content_type='text/json')

    elif req.method == 'PUT' and usr != None:
        id = req.GET.get('id')
        prod = list(Products.objects.filter(id=id).values())[0]
        dct = {"sku_name": prod["sku_name"], "sku_category": prod["sku_category"], "price": prod["price"]}
        body_unicode = req.body.decode('utf-8')
        payload = ast.literal_eval(body_unicode)[0]
        try:
            for keys, values in payload.items():
                dct[keys] = values
            Products.objects.filter(id=id).update(sku_name=dct["sku_name"], sku_category=dct["sku_category"],
                                                  price=dct["price"])
            res = json.dumps([{'message': 'changes affected one product!!!'}])
        except:
            res = json.dumps(([{'message': 'unable to update product!'}]))
        return HttpResponse(res, content_type='text/json')

    elif req.method == 'DELETE' and usr != None:
        id = req.GET.get('id')
        try:
            Products.objects.filter(id=id).delete()
            res = json.dumps([{'message': 'delted product successfully'}])
        except:
            res = json.dumps(([{'message': 'unable to delete product!'}]))
        return HttpResponse(res, content_type='text/json')
    else:
        res = json.dumps([{'Auth Error': 'Unauthenticated User!!!'}])
        return HttpResponse(res, content_type='text/json')


@csrf_exempt
def create(req):
    body_unicode = req.body.decode('utf-8')
    payload = ast.literal_eval(body_unicode)[0]
    user = payload['username']
    password = payload['password']
    usr = authenticate(username=user, password=password)
    if req.method == 'POST' and usr!=None:
        body_unicode = req.body.decode('utf-8')
        payload = ast.literal_eval(body_unicode)[0]
        id = payload['id']
        sku_name = payload['sku_name']
        sku_category = payload['sku_category']
        price = payload['price']
        if len(Products.objects.filter(id=id)) > 0:
            res = json.dumps([{'Error': 'Product ID exists'}])
        else:
            try:
                pro = Products(id=id, sku_name=sku_name, sku_category=sku_category, price=price)
                pro.save()
                res = json.dumps([{'Success': 'Product added successfully'}])
            except:
                res = json.dumps([{'Error': 'Product cant be added'}])
        return HttpResponse(res, content_type='text/json')
