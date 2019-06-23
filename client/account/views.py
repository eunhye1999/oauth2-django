from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.auth.models import User
from customoauth.models import  Providers, Social_applications, Social_token, Social_account

from oauthlib.common import UNICODE_ASCII_CHARACTER_SET
from oauthlib.common import generate_client_id as oauthlib_generate

import requests
import json

def login(request):
    context = {
        'login_provider':['unixdev']
    }
    return render(request, 'account/login.html', context)

@login_required
def profile(request):
    return HttpResponse("sadsadasd")


def genlink(provider_dict):
    link_provider = "?"
    for k, v in provider_dict.items():
        link_provider += "{}={}&".format(k,v)
    return link_provider[:-1]

import datetime

def set_cookie(response, key, value, days_expire = 1):
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds= days_expire *60 * 60), "%a, %d-%b-%Y %H:%M:%S GMT") # set expire 1 min
    response.set_cookie(key, value, expires=expires)
    return response

def redirect_login(request, provider):
    if(provider == 'unixdev'):
        provier_obj = Providers.objects.get(name=provider)
        # print(provier_obj)
        '''
            get client_id from database table : Social_application
        '''
        gen_satate = oauthlib_generate(length=40, chars=UNICODE_ASCII_CHARACTER_SET)

        provider_json = {
            "client_id" : "MOuXlkPCRF2H6I8Xe9MsuiH2I8FJ8jZbckL4HMRF",
            "response_type" : "code",
            "scope": "comment,write",
            "state": gen_satate,
            "redirect_uri": "{}/account/{}/login/callback".format(settings.URL_SITE, provider)
        }

        link_author = "{}/o2/authorize/{}".format(f"{provier_obj.url}", genlink(provider_json))  
        response = redirect(link_author)
        response = set_cookie(response,'state',gen_satate) 
    
    return response


def redirect_callback(request, provider):
    if(request.method == 'GET'):
        if 'state' in request.COOKIES:
            if(request.COOKIES['state'] == request.GET['state']):
                '''
                    POST CLIEND_SECRET to /o2/token/ for get accesstoken
                    response.status = 200
                    {
                        "access_token" : "XzltakjhjddfoiuhhasdeDFb",
                        "refresh_token" : "",
                        "token_type" : "bearer",
                        "scope" : "reqd,comment",
                        "expires" : "2019-06-20T12:28:44.851"
                    }
                '''
                provier_obj = Providers.objects.get(name=provider)
                applications_obj = Social_applications.objects.get(provider_id=provier_obj.id)

                data = {
                    'client_id': applications_obj.client_id, 
                    'client_secret': applications_obj.client_secret, 
                    'grat_type': "Authorization_code", 
                    'code': request.GET['code']
                } 

                access_token_post = requests.post(url = "{}/o2/token/".format(provier_obj.url), json = data) 
                request_status = access_token_post.status_code
                if(request_status == 200):
                    '''
                        GET information of user to /o2/info/ 
                        response.status = 200
                        {
                            "uid" : 50
                            "username" : topz,
                            "email": example@email.com
                        }
                    '''
                    access_token_body = json.loads(access_token_post.content.decode('utf-8'))
                    auth_token=access_token_body['access_token']
                    head = {
                        'Authorization': 'Bearer ' + auth_token,
                        'content-type': "application/json"
                    }
                    get_profile = requests.get("{}/o2/info/".format(provier_obj.url), headers=head)
                    request_status = get_profile.status_code
                    if(request_status == 200):
                        get_profile = json.loads(get_profile.content.decode('utf-8'))
                        social_acc_obj = Social_account.objects.filter(uid=get_profile['uid'])
                        context  = {
                            "application_id": applications_obj.id, 
                            "provider_id" : provier_obj.id,
                            "access_token": access_token_body['access_token'],
                            "expire":  access_token_body['expires']
                        }
                        if social_acc_obj:
                            print("have id social account")
                            context['user_id'] = social_acc_obj[0].user.id
                            
                        else:
                            print("No have id social account")
                            print(get_profile)
                            context['user_id'] = register(get_profile, context)
                        
                        insert_social_token(context)

                        auth_login(request, User.objects.get(pk=context['user_id']), backend='django.contrib.auth.backends.ModelBackend')

                        return redirect("/account/profile/")
                    
                    
                response = HttpResponse("status : {}".format(request_status))
                response.delete_cookie('state')
                return response
                
            # else:
            #     response = HttpResponse("state wrong")
            #     response.delete_cookie('state')
            #     return response
        
            return HttpResponse("Error state worg OR no have state in cach")


def register(dataCon, data):
    '''
        register in local database
    '''
    user_object = User(
            username=dataCon["email"],
            email=dataCon["email"],
            first_name=dataCon['username']
    )
    user_object.save()
    social_acc = Social_account(
            user_id=user_object.id,
            uid=dataCon["uid"], 
            provider_id=data["provider_id"]
    )
    social_acc.save()
    return user_object.id

def insert_social_token(data):
    social_token = Social_token(
            user_id=data['user_id'],
            token=data['access_token'],
            expire=data['expire'],
            application_id=data['application_id'],
    )
    social_token.save()