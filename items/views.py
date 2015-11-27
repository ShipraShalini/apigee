from django.http import HttpResponse
from datetime import datetime
from items.models import Items, bids


def add_items(request):
    if request.method == "POST":
        item= Items.objects.create(name = request.POST['name'],
                                    date_added = datetime.now(),
                                    image= request.POST['image_url'])
        return HttpResponse("Added Item: {}".format(item.name), status= 200)


def del_items(request):
    item_name=request.REQUEST['name']
    Items.objects.get(name = item_name).delete()
    return HttpResponse("OK 200 Item deleted {}".format(item_name), status= 200)


def view_items(request):
    item_name=request.REQUEST['name']
    item = Items.objects.get(name = item_name)
    #find top 5 bids
    return HttpResponse("OK 200 Item Listed: {}".format(item), status= 200)


def add_bid(request):
    if request.method == "POST":
        bid = bids.objects.create(bidder = request.POST['name'],  #find out way of retrieving user form login info
                                    item = request.POST['item'],
                                    bid_amount= request.POST['amount'])
        #function for notifying bidders

        return HttpResponse("Added Item: {} {}".format(bid.item, bid.bid_amount), status= 200)


def del_bids(request):
    item_name=request.REQUEST['name']
    bidder = request.REQUEST['name']
    bids.objects.get(Q(name__exact = item_name),
                     Q(bidder__exact = bidder  )).delete()
    return HttpResponse("OK 200 Bid deleted {} for ".format(item_name), status= 200)


def view_bids(request):
    bidder=request.REQUEST['name']
    bid_list = bids.objects.filter(name = bidder)
    return HttpResponse("OK 200 \nBids Listed: {}".format(bid_list), status= 200)
