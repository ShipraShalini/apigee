from view_helper import notify,read_request_item, is_sold
from items.ES.constants import messages
from django.contrib.auth.decorators import login_required
from elastic import get_bid , create_bid, modify_bid


@login_required(login_url='http://localhost:8000/login_message/')
def add_bid(request):
    bidder, item_name, amount = read_request_item(request)
    #Check if item is sold
    if is_sold(item_name):
        return messages['SOLD_MESSAGE']
    #search for the bid using bidder and item_name
    bid = get_bid(bidder = bidder, item_name=item_name)
    #if bid is present update the bid amount else create bid
    if bid:
        bid = modify_bid(bid=bid[0], amount=amount)
        bid_action="Modified"
    else:
        bid = create_bid(item = item_name, bidder = bidder, bid_amount= amount)
        bid_action="Created"

    #notify all bidders for this item
    notify(item= item_name, username= bidder, bid_amount= amount)

    return "{0} Bid: {1} {2}".format(bid_action, bid.item, bid.bid_amount)


'''
{"item" : "item_name"}
'''
@login_required(login_url='http://localhost:8000/login_message/')
def del_bids(request):
    bidder, item_name = read_request_item(request)
    print bidder,item_name
    bid = get_bid(bidder= bidder, item_name = item_name)
    if bid:
        bid[0].delete()
        message = messages['BID_DELETED_MESSAGE']
    else:
        message = messages['BID_NOT_PRESENT_MESSAGE']
    return message


'''
no input, users should be logged in
'''
#view bids of an users
@login_required(login_url='http://localhost:8000/login_message/')
def view_bids(request):
    bidder, item_name = read_request_item(request)
    bid_dict= {}
    bid_list = get_bid(bidder=bidder)
    for bid in bid_list:
        print type(bid)
        bid_dict[bid.item] = int(bid.bid_amount)
    return "User: {0} \nBids: \n{1}".format(bidder, bid_dict)
