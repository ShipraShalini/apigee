from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json

def welcome(request):
    return ("Welcome to Bidding Engine")

def login_message(request):
    return ("Please log in")


def add(request):
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
    return ("Added User: {0} {1}".format(username,email))


@login_required(login_url='http://localhost:8000/login_message/')
def modify(request):
    username = request.user
    newname= json.loads(request.body)['newname']
    u = User.objects.get(username=username)
    u.username = newname
    u.save()
    return ("username modified")


@login_required(login_url='http://localhost:8000/login_message/')
def delete(request):
    username = request.user
    User.objects.get(username=username).delete()
    return ("User {0} deleted".format(username))


@login_required(login_url='http://localhost:8000/login_message/')
def view(request):
    username = request.user
    user = User.objects.get(username=username)
    return ("username= {0},\nfirst_name= {1},\nlast_name = {2},\nemail= {3}".format(user.username, user.first_name, user.last_name, user.email))






