from django.http import HttpResponse, HttpResponseRedirect
from items.models import Items
from datetime.datetime import datetime


def add_items(request):
    seller = request.user
    if seller:
        if request.method == "POST": #find way to pass null to image_url
            item= Items.objects.create(name = request.POST['name'],
                                       seller = seller,
                                       date_added = datetime.now(),
                                        min_bid = request.POST['min_bid'] )
            return HttpResponse("Added Item: {}".format(item.name), status= 200)

    else:
        return HttpResponseRedirect("/user_login/") #redirect to login