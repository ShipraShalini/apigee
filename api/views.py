from django.http import HttpResponse
from django.contrib.auth.models import User


def add_user(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        User.objects.create_user( name, email, 'johnpassword')
        return HttpResponse("Added User: {} {}".format(name,email))
    else:
        return HttpResponse("Add User")



