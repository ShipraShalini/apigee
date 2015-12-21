from items.ES.items_views import add_items, view_items, del_items
from django.http import HttpResponse

def item(request):
    if request.method == "GET":
        print "p", request.GET
        message = view_items(request)

    if request.method == "POST":
        message= add_items(request)

    if request.method == "DELETE":
        message = del_items(request)

    return HttpResponse(message ,status=200)
