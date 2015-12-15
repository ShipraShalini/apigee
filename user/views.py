from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def add_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        User.objects.create_user( username= username,
                                  first_name= first_name,
                                  last_name = last_name,
                                  email=email,
                                  password='johnpassword'
                                  )
        return HttpResponse("Added User: {0} {1}".format(username,email), status= 200)
    else:
        return HttpResponse("Add User")

@csrf_exempt
def user_login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse("User logged in", status= 200)
        else:
            # Return a 'disabled account' error message
            return HttpResponse("User not logged in")
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("Invalid login")


def user_logout(request):
    logout(request)


def user_delete(request):
    username = request.user
    if username:
        User.objects.get(username=username).delete()
        return HttpResponse("User {0} deleted".format(username))
    else:
        return HttpResponse("Please login")
@csrf_exempt
def user_modify(request):
    username = request.user
    if username:
        newname= json.loads(request.body)['newname']
        u = User.objects.get(username=username)
        u.username = newname
        u.save()
        return HttpResponse("username modified")
    else:
        return HttpResponse("Please log in")
