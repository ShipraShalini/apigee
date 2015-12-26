from src.common.helpers.getrequest import read_request_item
from src.api.ES.helpers.commonhelper import notify, is_sold
from items.ES.constants import messages
from django.contrib.auth.decorators import login_required
from src.api.ES.helpers.bidhelper import *



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