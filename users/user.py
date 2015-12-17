from views import add, modify, delete, view
from django.http import HttpResponse


def user(request):
    if request.method == "GET":
        message = view(request)

    if request.method == "POST":
        message = add(request)

    if request.method == "PUT":
        message = modify(request)

    if request.method == "DELETE":
        message = delete(request)

    return HttpResponse(message)
