from items_views import add_items, view_items, del_items, update_items
from django.http import HttpResponse

def item(request):

    if request.method == "GET":
        message = view_items(request)

    if request.method == "POST":
        message= add_items(request)

    if request.method == "DELETE":
        message = del_items(request)

    if request.method == "PUT":
        message = update_items(request)

    return HttpResponse(message)