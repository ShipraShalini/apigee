from django.http import HttpResponse
from django.db.models import Max
from datetime import datetime, time, timedelta
from items.models import Items, bids
from view_helper import notify
from elastic import add_doc
from es_models import Item

def welcome(request):
    return HttpResponse("Welcome to Bidding Engine", status= 200)

def add_items(request):
    seller = request.user
    if seller:
        if request.method == "POST":
            item_name =  request.POST['name']
            #find way to pass null to image_url
            item = { "item_name" : item_name,
                     "seller" : seller,
                     "status" : "Available",
                     "date_added" : datetime.now(),
                     "min_bid" : request.POST['min_bid']
                     }
            res = add_doc(index= 'item', type=Item, id = item_name, doc= item)


            from apscheduler.scheduler import Scheduler

            sched = Scheduler()
            sched.start()
            exec_time= datetime.now() + timedelta(seconds=5)
            job1 = sched.add_date_job(sell_items, exec_time, [item_name])


            return HttpResponse("Added Item: {}".format(item_name), status= 200)

    else:
        return HttpResponse("Please log in") #redirect to login


#Is payement logic required?
def sell_items(index, item_id):
    res = Item.get(index=index, id = item_id)
    #find max bid
    res1 = Item.update(index= index,  id= item_id, body = {"doc": {"status": "Sold"}})
    return HttpResponse("Item Sold: {} at {}".format(item_id, selling_price), status= 200)


def del_items(request):
    item_id=request.REQUEST['name']
    res= Item.delete(index='item', id = item_id)
    return HttpResponse("Item deleted {}".format(item_id), status= 200)


def view_items(request):
    item_id=request.REQUEST['name']
    item = Item.get(index='item', id = item_id)
    if item.status == "Sold":
        return HttpResponse("Item Listed: {} \\n DateCreated: {} \\n Status: {}".format(item.name,
                                                                                        item.date_added,
                                                                                        item.status),
                            status= 200)

    else:
        #find top 5 bids
        top5=[]
        top5_result = bids.objects.filter(item_name = item_name).order_by('-bid_amount')[:5]
        for bid in top5_result:
            top5.append({'Bidder':bid.bidder, 'Item':bid.item.name, 'Bid Amount': bid.bid_amount})

        return HttpResponse("OK 200 Item Listed: {} \\n DateCreated: {} \\n The top 5 bids: \\n {}".format(item.name,
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
                return HttpResponse("Cannot Bid: {}. Item already sold".format(item_name), status= 200)

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

                return HttpResponse("Added Bid: {} {}".format(bid.item, bid.bid_amount), status= 200)
    else:
        return HttpResponse("Please log in")


def del_bids(request):
    bidder = request.user
    if bidder:
        item_name=request.REQUEST['item']
        try:
            bids.objects.get(item___exact = item_name,bidder__exact = bidder).delete()
        except:
            return HttpResponse("Error: could not delete item {}. Retry".format(item_name))
        else:
            return HttpResponse("OK 200 Bid deleted {} for ".format(item_name), status= 200)
    else:
        return HttpResponse("Please log in")


#is it needed
def view_bids(request):
    bidder = request.user
    if bidder:
        bid_list = bids.objects.filter(bidder = bidder)
        for bid in bid_list:
            print "print bid:" ,bid.item.name, bid.bidder, bid.bid_amount
        return HttpResponse("Bids Listed: {}".format(bid_list), status= 200)
    else:
        return HttpResponse("Please log in")

