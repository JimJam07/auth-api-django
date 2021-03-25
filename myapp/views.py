from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import ast
import jwt

from myapp.models import User


def index(req):
    res = json.dumps([{}])
    return HttpResponse(res, content_type='text/json')


# url structure login?
def login(req):
    if req.method == 'GET':
        name = req.GET.get('userName')
        pwd = req.GET.get('password')
        try:
            my_token = jwt.encode({'pwd': pwd}, 'kilofarm')
            user = list(User.objects.filter(name=name, pwd=my_token).values())[0]
            print(user)
            res = json.dumps([{'Success': 'User Authorized!!', 'jwt token': user['pwd']}])
        except:
            res = json.dumps([{'Error':'User not Found!!!'}])
    return HttpResponse(res, content_type='text/json')

@csrf_exempt
def signup(req):
    if req.method == 'POST':
        body_unicode = req.body.decode('utf-8')
        payload = ast.literal_eval(body_unicode)[0]
        name = payload['username']
        pwd = payload['password']
        dob = payload['DOB']
        phone_number = payload['phoneNumber']
        my_token = jwt.encode({'pwd': pwd}, 'kilofarm')
        if len(User.objects.filter(name=name)) > 0:
            res = json.dumps([{'Error': 'user name already exists'}])
        else:
            try:
                user = User(name=name, pwd=my_token,dob=dob,phoneNumber=phone_number)
                user.save()
                # usr = User.objects.filter(name=name, pwd=my_token)
                # print(usr)
                res = json.dumps([{'Success': 'User successfully added to database!!'}])
            except:
                res = json.dumps([{'Error': 'User Cant be added at this time'}])
        return HttpResponse(res, content_type='text/json')


# sample data
# [{
#     "username":"trans",
#     "password":"pass",
#     "DOB":"1/1/1",
#     "phoneNumber":999999
# }]