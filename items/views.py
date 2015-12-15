from django.http import HttpResponse
from django.db.models import Max
from datetime import datetime, time, timedelta
from items.models import Items, bids
from view_helper import notify
import json

def welcome(request):
    return HttpResponse("Welcome to Bidding Engine", status= 200)




'''
{
    "item": "item_name",
    "min_bid" : 1222
}
'''
def add_items(request):
    seller = request.user
    if seller:
        if request.method == "POST":
            #find way to pass null to image_url
            data = json.loads(request.body)
            item_name = data['item']
            seller = seller
            item= Items.objects.create(item_name = item_name,
                                       seller = seller,
                                       date_added = datetime.now(),
                                        min_bid = data['min_bid'] )

            # from apscheduler.scheduler import Scheduler
            #
            # sched = Scheduler()
            # sched.start()
            # exec_time= datetime.now() + timedelta(seconds=5)
            # job1 = sched.add_date_job(sell_items, exec_time, [item_name])
            #
            #
            return HttpResponse("Added Item: {0}".format(item.item_name), status= 200)

    else:
        return HttpResponse("Please log in") #redirect to login


#Is payement logic required?
def sell_items(item_name):
    item = Items.objects.get(item_name = item_name)
    selling_price = bids.objects.filter(item = item).aggregate(Max('bid_amount'))
    item.status = "Sold"
    item.save()
    return HttpResponse("Item Sold: {0} at {1}".format(item.name, selling_price), status= 200)


def del_items(request):
    item_name = json.loads(request.body)['item']
    Items.objects.get(item_name = item_name).delete()
    return HttpResponse("Item deleted {0}".format(item_name), status= 200)


def view_items(request):
    item_name=request.REQUEST['name']
    item = Items.objects.get(item_name = item_name)
    if item.status == "Sold":
        return HttpResponse("Item Listed: {0} \\n DateCreated: {1} \\n Status: {2}".format(item.name,
                                                                                        item.date_added,
                                                                                        item.status),
                            status= 200)

    else:
        #find top 5 bids
        top5=[]
        top5_result = bids.objects.filter(item_name = item_name).order_by('-bid_amount')[:5]
        for bid in top5_result:
            top5.append({'Bidder':bid.bidder, 'Item':bid.item.name, 'Bid Amount': bid.bid_amount})

        return HttpResponse("OK 200 Item Listed: {0} \\n DateCreated: {1} \\n The top 5 bids: \\n {2}".format(item.name,
                                                                                                           item.date_added,
                                                                                                           top5),
                            status= 200)







def add_bid(request):
    #input item, amount
    bidder = request.user
    if bidder:
        if request.method == "POST":
            item_name = request.POST['item']
            item = Items.objects.get(item_name = item_name)
            if item.status == 'Sold':
                return HttpResponse("Cannot Bid: {0}. Item already sold".format(item_name), status= 200)

            else:
                bid_amount= request.POST['amount']

                try:
                    bid = bids.objects.get(item = item, bidder = bidder )

                except bids.DoesNotExist:
                    bid = bids.objects.create(bidder = bidder,
                                            item = item,
                                            bid_amount= bid_amount)
                else:
                    bid.bid_amount = bid_amount
                    bid.save()
                    print"edited"

                #function for notifying bidders
                notify(item= item_name, username= bidder, bid_amount= bid_amount)

                return HttpResponse("Added Bid: {0} {1}".format(bid.item, bid.bid_amount), status= 200)
    else:
        return HttpResponse("Please log in")


def del_bids(request):
    bidder = request.user
    if bidder:
        item_name=request.REQUEST['item']
        try:
            bids.objects.get(item___exact = item_name,bidder__exact = bidder).delete()
        except:
            return HttpResponse("Error: could not delete item {0}. Retry".format(item_name))
        else:
            return HttpResponse("OK 200 Bid deleted {0} for ".format(item_name), status= 200)
    else:
        return HttpResponse("Please log in")


#is it needed
def view_bids(request):
    bidder = request.user
    if bidder:
        bid_list = bids.objects.filter(bidder = bidder)
        for bid in bid_list:
            print "print bid:" ,bid.item.name, bid.bidder, bid.bid_amount
        return HttpResponse("Bids Listed: {0}".format(bid_list), status= 200)
    else:
        return HttpResponse("Please log in")

