from django.http import HttpResponse
from datetime import datetime
from 


def add_items(request):
    if request.method == "POST":
        item
        name = request.POST['name']
        date_added = datetime.now()

        return HttpResponse("Added User: {} {}".format(name,email))

    return HttpResponse("OK 200 Items Added")

def del_items(request):
    return HttpResponse("OK 200 Item deleted")

def view_items(request):
    return HttpResponse("OK 200 Items Listed")