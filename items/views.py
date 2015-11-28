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
    top5=[]

    #find top 5 bids
    top5_result = bids.objects.filter(item = item_name).order_by('-bid_amount')[:5]
    for bid in top5_result:
        top5.append({'Bidder':bid.bidder, 'Item':bid.item.name, 'Bid Amount': bid.bid_amount})

    return HttpResponse("OK 200 Item Listed: {} \\n DateCreated: {} \\n The top 5 bids: \\n {}".format(item.name,
                                                                                                       item.date_added,
                                                                                                       top5),
                        status= 200)


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
    #create a time left function
    #create function to view to 5

    return HttpResponse("OK 200 \nBids Listed: {}".format(bid_list), status= 200)
