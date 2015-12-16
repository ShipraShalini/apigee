from django.http import HttpResponse
from django.db.models import Max
from datetime import datetime, time, timedelta
from time import strftime
from items.models import Items, bids
from view_helper import notify, scheduler
import json, types
import logging
from django.contrib.auth.decorators import login_required


logging.basicConfig()

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
    seller = request.user
    if request.method == "POST":
        #find way to pass null to image_url
        data = json.loads(request.body)
        item_name = data['item']
        seller = seller

        item= Items.objects.create(item_name = item_name,
                                   seller = seller,
                                   date_added = datetime.now(),
                                    min_bid = data['amount'] )

        exec_time= datetime.now() + timedelta(minutes= 1)
        s.addjob(function=sell_items, time= exec_time, arguments=[item])
        print exec_time
        return HttpResponse("Added Item: {0}".format(item.item_name), status= 200)


#Is payement logic required?
@login_required(login_url='http://localhost:8000/login_message/')
def sell_items(item):
    print "in selling function"
    selling_price = bids.objects.filter(item=item).aggregate(Max('bid_amount'))['bid_amount__max']
    print selling_price
    buyer = bids.objects.get(item=item, bid_amount = selling_price).bidder
    item.status = "Sold"
    item.save(update_fields=['status'])
    print("Item Sold: {0} at {1} to {2}".format(item.item_name, selling_price, buyer))
    #return HttpResponse("Item Sold: {0} at {1} to {2}".format(item.item_name, selling_price, buyer), status= 200)

@login_required(login_url='http://localhost:8000/login_message/')
def del_items(request):
    seller = request.user
    if seller:
        item_name = json.loads(request.body)['item']
        Items.objects.get(item_name = item_name).delete()
        return HttpResponse("Item deleted {0}".format(item_name), status= 200)
    else:
        return HttpResponse("Please log in")


@login_required(login_url='http://localhost:8000/login_message/')
def view_items(request):
    data = json.loads(request.body)
    item_name = data['item']
    item = Items.objects.get(item_name = item_name)
    if item.status == "Sold":
        return HttpResponse("Item Listed: {0} \\n DateCreated: {1} \\n Status: {2}".format(item.name,
                                                                                    item.date_added.strftime("%A, %B %d %Y, %H:%M:%S"),
                                                                                    item.status),
                        status= 200)

    else:
        #find top 5 bids
        top5={}
        i=1
        top5_result = bids.objects.filter(item__item_name__exact = item_name).order_by('-bid_amount')[:5]
        for bid in top5_result:
            top5[i]=({'Bidder':bid.bidder, 'Item':bid.item.item_name, 'Bid Amount': int(bid.bid_amount)}) #int to remove L character from output
            i=i+1

        return HttpResponse("OK 200 Item Listed: {0} \nDateCreated: {1} \nThe top 5 bids:\n{2}".format(item.item_name,
                                                                                                           item.date_added.strftime("%A, %B %d %Y, %H:%M:%S"),
                                                                                                           top5),
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
    bidder = request.user
    if bidder.is_authenticated() :
        if request.method == "POST":
            data = json.loads(request.body)
            item_name = data['item']
            item = Items.objects.get(item_name = item_name)
            if item.status == 'Sold':
                return HttpResponse("Cannot Bid: {0}. Item already sold".format(item_name), status= 200)

            else:
                bid_amount= data['amount']

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

                return HttpResponse("Added Bid: {0} {1}".format(bid.item.item_name, bid.bid_amount), status= 200)
    else:
        return HttpResponse("Please log in")

'''
{
    "item" : "item_name"
}
'''
@login_required(login_url='http://localhost:8000/login_message/')
def del_bids(request):
    bidder = request.user
    if bidder:
        item_name=json.loads(request.body)['item']
        try:
            bids.objects.get(item__item_name__exact = item_name, bidder__exact = bidder).delete()
        except:
            return HttpResponse("Error: could not delete item {0}. Retry".format(item_name))
        else:
            return HttpResponse("Bid deleted for {0} ".format(item_name), status= 200)
    else:
        return HttpResponse("Please log in")

'''
no input, users should be logged in
'''
#view bids of an users
@login_required(login_url='http://localhost:8000/login_message/')
def view_bids(request):
    bidder = request.user
    bid_dict={}
    if bidder:
        bid_list = bids.objects.filter(bidder = bidder)
        for bid in bid_list:
              bid_dict[bid.item.item_name]= int(bid.bid_amount)

        return HttpResponse("User: {0} \nBids: \n{1}".format(request.user, bid_dict), status= 200)
    else:
        return HttpResponse("Please log in")


#check this
# for k,v in globals().items():
#     if isinstance(v, types.FunctionType):
#         print k,":", v
#         globals()[k] = login_required(function=v, login_url='http://localhost:8000/login_message/' )


