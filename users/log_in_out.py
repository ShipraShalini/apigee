from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json



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
    if request.method == "GET":
        user= request.user.get_username()
        print user
        logout(request)
        return HttpResponse("User {0} logged out".format(user))
