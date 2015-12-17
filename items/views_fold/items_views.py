from django.http import HttpResponse
from items.models import Items,bids
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from view_helper import read_request_item, scheduler, is_sold, Highestbid

s = scheduler()

@login_required(login_url='http://localhost:8000/login_message/')
def add_items(request):
    seller, item_name, min_bid = read_request_item(request)
    item= Items.objects.create(item_name = item_name, seller = seller, date_added = datetime.now(), min_bid = min_bid )
    exec_time= datetime.now() + timedelta(minutes = 1)
    s.addjob(function=sell_items, time= exec_time, arguments=[item])
    return HttpResponse("Added Item: {0}".format(item.item_name), status= 200)


#Is payement logic required?

@login_required(login_url='http://localhost:8000/login_message/')
def sell_items(item):
    selling_price = bids.objects.filter(item=item).aggregate(Max('bid_amount'))['bid_amount__max']
    buyer = bids.objects.get(item=item, bid_amount = selling_price).bidder
    item.status = "Sold"
    item.save(update_fields=['status'])
    print("Item Sold: {0} at {1} to {2}".format(item.item_name, selling_price, buyer))
    #return HttpResponse("Item Sold: {0} at {1} to {2}".format(item.item_name, selling_price, buyer), status= 200)


@login_required(login_url='http://localhost:8000/login_message/')
def del_items(request):
    seller, item_name = read_request_item(request)
    try:
        Items.objects.get(item_name = item_name, seller= seller).delete()
    except Items.DoesNotExist:
        return HttpResponse("Item {0} not present".format(item_name), status= 200)
    else:
        return HttpResponse("Item deleted {0}".format(item_name), status= 200)


@login_required(login_url='http://localhost:8000/login_message/')
def view_items(request):
    seller, item_name = read_request_item(request)
    item = Items.objects.get(item_name = item_name)
    date = item.date_added.strftime("%A, %B %d %Y, %H:%M:%S")
    message= "Item Listed: {0} \\n DateCreated: {1} \\n Status: {2}".format(item.name, date, item.status)
    if is_sold(item):
        return HttpResponse(message, status= 200)
    else:
        top_bids= Highestbid(N=5, item=item)
        return HttpResponse(message + "The top 5 bids:\n{2}".format(item.item_name, date, top_bids), status= 200)
