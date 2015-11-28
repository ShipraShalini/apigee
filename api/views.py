from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def add_user(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        User.objects.create_user( name, email, 'johnpassword')
        return HttpResponse("Added User: {} {}".format(name,email), status= 200)
    else:
        return HttpResponse("Add User")


def user_login(request):
    name = request.POST['name']
    password = request.POST['password']
    user = authenticate(username=name, password=password)
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
    pass

def user_modify(request):
    pass
