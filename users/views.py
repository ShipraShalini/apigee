from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

def welcome(request):
    return HttpResponse("Welcome to Bidding Engine", status= 200)

def login_message(request):
    return HttpResponse("Please log in")

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


def user_login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse("User {0} logged in".format(request.user), status= 200)
        else:
            # Return a 'disabled account' error message
            return HttpResponse("User not logged in")
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("Invalid login")


@login_required(login_url='http://localhost:8000/login_message/')
def user_logout(request):
    user= request.user
    logout(request)
    return HttpResponse("User {0} logged out".format(user))


@login_required(login_url='http://localhost:8000/login_message/')
def user_delete(request):
    username = request.user
    User.objects.get(username=username).delete()
    return HttpResponse("User {0} deleted".format(username))


'''
{
        "newname": "brad"
}
'''

@login_required(login_url='http://localhost:8000/login_message/')
def user_modify(request):
    username = request.user
    newname= json.loads(request.body)['newname']
    u = User.objects.get(username=username)
    u.username = newname
    u.save()
    return HttpResponse("username modified")

