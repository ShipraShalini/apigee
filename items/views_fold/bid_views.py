from items.models import Items, bids
from view_helper import notify,read_request_item, is_sold
from django.contrib.auth.decorators import login_required



@login_required(login_url='http://localhost:8000/login_message/')
def add_bid(request):
    bidder, item_name, amount = read_request_item(request)
    item = Items.objects.get(item_name = item_name)
    if is_sold(item):
        return ("Cannot Bid: {0}. Item already sold".format(item_name))
    else:
        bid_amount = amount
        try:
            bid = bids.objects.get(item = item, bidder = bidder )
        except bids.DoesNotExist:
            bid = bids.objects.create(bidder = bidder, item = item, bid_amount= bid_amount)
            bid_action="Created"
        else:
            bid.bid_amount = bid_amount
            bid.save(update_fields=['bid_amount'])
            bid_action="Modified"

        #function for notifying bidders
        notify(item= item_name, username= bidder, bid_amount= bid_amount)

        return ("{0} Bid: {1} {2}".format(bid_action,bid.item.item_name, bid.bid_amount))


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
        return ("Error: could not delete bid {0}. Bid not present".format(item_name))
    else:
        return ("Bid deleted for {0} ".format(item_name))


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

    return ("User: {0} \nBids: \n{1}".format(bidder, bid_dict))
