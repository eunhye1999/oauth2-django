from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse

from oauth2db.models import  Application, Accesstgrant, Accesstoken
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from oauthlib.common import UNICODE_ASCII_CHARACTER_SET
from oauthlib.common import generate_client_id as oauthlib_generate

import numpy as np
import json
import datetime
import hashlib 

def genlink(provider_dict):
    link_provider = "?"
    for k, v in provider_dict.items():
        link_provider += "{}={}&".format(k,v)
    return link_provider[:-1]

@login_required
def authorize(request):
    if(request.method == "GET"):
        '''
            ดู client_id id และ scope ใน database และส่งหน้า page allow หรือ reject
            scope_of_user คิดว่าจะกลอง user เผื่อไว้สำหรับจะทำกับ project true
        '''
        obj_app = Application.objects.get(client_id= request.GET['client_id'])
        scope_of_user = ['read','write','comment','vote'] 
        # import pdb; pdb.set_trace()
        scope = np.intersect1d(request.GET['scope'].split(','), scope_of_user)
        context = {
            "user_name" : request.user,
            "scope_ary" : scope,
            "scope_str" : ",".join(scope),
            "application" : obj_app.id,
            "user" : request.user.id,
            "redirect": obj_app.redirect_uri
        }
        return render(request, 'oauth2/allow.html', {'context' : context})
        
    elif(request.method == "POST"):
        '''
            get callback url form database และ gen code
        '''
        data = request.POST
        json_link = {
            'code' : oauthlib_generate(length=40, chars=UNICODE_ASCII_CHARACTER_SET),
            'state' : request.POST['state']
        }
        obj_accesstgrant = Accesstgrant(
            user_id = int(data['user']), 
            application_id = int(data['application']),
            code = json_link['code'],
            scope = data['scope'],
            expires = datetime.datetime.now() - datetime.timedelta(minutes=60), # 1 ช.ม.
            redirect_uri = data['redirect'],
        )

        obj_accesstgrant.save()

        # link_author = "{}/account/unixdev/login/callback/{}".format('http://127.0.0.1:3200', genlink(json_link))  
        link_author = "{}{}".format(data['redirect'], genlink(json_link))  

        return redirect(link_author)

@csrf_exempt
def token(request):
    if(request.method == "POST"):
        body = json.loads(request.body.decode('utf-8'))
        grant_obj = Accesstgrant.objects.filter(code = body['code'])
        if(grant_obj):
            grant = grant_obj[0]
            app_obj = Application.objects.get(pk=grant.application.id) 
            if(app_obj.client_secret == body['client_secret']):
                context = {
                    "access_token" : oauthlib_generate(length=40, chars=UNICODE_ASCII_CHARACTER_SET),
                    "refresh_token" : "",
                    "token_type" : "bearer",
                    "scope" : grant.scope,
                    "expires" : datetime.datetime.now() - datetime.timedelta(minutes=60)
                }
                '''
                    insert access_token to database 
                '''
                obj_accesstgrant = Accesstoken(
                    user_id = grant.user.id, 
                    application_id = grant.application.id,
                    token = context['access_token'],
                    scope = context['scope'],
                    expires = context['expires']
                )

                obj_accesstgrant.save()

                return JsonResponse(context)

            return JsonResponse({"secret_id":"not match secret id"})

        return JsonResponse({"grant":"not match code"})
    
def infomation(request):
    '''
        check accesstoken for get profile user
    '''
    if(request.method == "GET"):
        hearder_author = request.headers["Authorization"].split() 
        if(hearder_author[0] == "Bearer"):
            access_obj = Accesstoken.objects.filter(token=hearder_author[1])
            if access_obj:
                user_obj = User.objects.get(pk = access_obj[0].user.id)
                context = {
                    "uid" : user_obj.id,
                    "username" : user_obj.username,
                    "email": user_obj.email
                }
                return JsonResponse(context)
        