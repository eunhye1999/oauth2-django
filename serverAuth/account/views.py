from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
    if(request.method == "POST"):
        # import pdb; pdb.set_trace()
        user_id = request.POST['id']
        user_pass = request.POST['password']
        user = authenticate(request, username=user_id, password=user_pass)
        if user:
            auth_login(request, user)
            if 'next' in request.POST:
                link_get_next = request.POST['next']
                print(link_get_next)
                return redirect(link_get_next)
            else:
                print('except')
                return JsonResponse({"singin":"success"}, safe=False)
        else:
            return JsonResponse({"singin":"fail"}, safe=False)
            # return render(request, 'account/failform.html')
        
    elif(request.method == "GET"):
        print("loginForm")
        return render(request, 'account/loginform.html')
    
def logout(request):
    auth_logout(request)
    return render(request, 'account/loginform.html')
