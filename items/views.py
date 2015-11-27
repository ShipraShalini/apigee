from django.http import HttpResponse
from datetime import datetime
from items.models import Items, bids


def add_items(request):
    if request.method == "POST":
        item= Items.objects.create(name = request.POST['name'],
                                    date_added = datetime.now(),
                                    image= request.POST['image_url'])
        return HttpResponse("Added Item: {} {}".format(item.name))

    return HttpResponse("OK 200 Items Added")

def del_items(request):
    return HttpResponse("OK 200 Item deleted")

def view_items(request):
    return HttpResponse("OK 200 Items Listed")