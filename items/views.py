from django.http import HttpResponse
from django.db.models import Max
from datetime import datetime, time, timedelta
from time import strftime
from items.models import Items, bids
from view_helper import notify, scheduler, Highestbid, read_request_item, is_sold
import json
from django.contrib.auth.decorators import login_required




def welcome(request):
    return HttpResponse("Welcome to Bidding Engine", status= 200)

def login_message(request):
    return HttpResponse("Please log in")

s = scheduler()

'''
{
    "item": "item_name",
    "amount" : 1222
}
'''


@login_required(login_url='http://localhost:8000/login_message/')
def add_items(request):
    seller, item_name, min_bid = read_request_item(request)

    item= Items.objects.create(item_name = item_name,
                               seller = seller,
                               date_added = datetime.now(),
                                min_bid = min_bid )

    exec_time= datetime.now() + timedelta(minutes= 1)
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
    except Exception as e:
        print e
    else:
        return HttpResponse("Item deleted {0}".format(item_name), status= 200)



@login_required(login_url='http://localhost:8000/login_message/')
def view_items(request):
    seller, item_name = read_request_item(request)
    item = Items.objects.get(item_name = item_name)
    if is_sold(item):
        return HttpResponse("Item Listed: {0} \\n DateCreated: {1} \\n Status: {2}".format(item.name,
                                                                                    item.date_added.strftime("%A, %B %d %Y, %H:%M:%S"),
                                                                                    item.status),
                        status= 200)

    else:
        top_bids= Highestbid(N=5, item=item)
        return HttpResponse("OK 200 Item Listed: {0} \nDateCreated: {1} \nThe top 5 bids:\n{2}".format(item.item_name,
                                                                                                           item.date_added.strftime("%A, %B %d %Y, %H:%M:%S"),
                                                                                                           top_bids),
                            status= 200)


'''
{
    "item": "abc",
    "amount" : 34344
}
'''
@login_required(login_url='http://localhost:8000/login_message/')
def add_bid(request):
    #input item, amount
    bidder, item_name, amount = read_request_item(request)
    item = Items.objects.get(item_name = item_name)

    if is_sold(item):
        return HttpResponse("Cannot Bid: {0}. Item already sold".format(item_name), status= 200)

    else:
        bid_amount= amount

        try:
            bid = bids.objects.get(item = item, bidder = bidder )

        except bids.DoesNotExist:
            bid = bids.objects.create(bidder = bidder,
                                    item = item,
                                    bid_amount= bid_amount)
            bid_action="Created"
        else:
            bid.bid_amount = bid_amount
            bid.save(update_fields=['bid_amount'])
            bid_action="Modified"

        #function for notifying bidders
        notify(item= item_name, username= bidder, bid_amount= bid_amount)

        return HttpResponse("{0} Bid: {1} {2}".format(bid_action,bid.item.item_name, bid.bid_amount), status= 200)


'''
{
    "item" : "item_name"
}
'''
@login_required(login_url='http://localhost:8000/login_message/')
def del_bids(request):
    bidder, item_name = read_request_item(request)
    try:
        bids.objects.get(item__item_name__exact = item_name, bidder__exact = bidder).delete()
    except bids.DoesNotExist:
        return HttpResponse("Error: could not delete bid {0}. Bid not present".format(item_name))
    else:
        return HttpResponse("Bid deleted for {0} ".format(item_name), status= 200)


'''
no input, users should be logged in
'''
#view bids of an users
@login_required(login_url='http://localhost:8000/login_message/')
def view_bids(request):
    bidder, item_name = read_request_item(request)
    bid_dict={}
    bid_list = bids.objects.filter(bidder__exact = bidder)
    for bid in bid_list:
          bid_dict[bid.item.item_name]= int(bid.bid_amount)

    return HttpResponse("User: {0} \nBids: \n{1}".format(bidder, bid_dict), status= 200)



#check this
# for k,v in globals().items():
#     if isinstance(v, types.FunctionType):
#         print k,":", v
#         globals()[k] = login_required(function=v, login_url='http://localhost:8000/login_message/' )


