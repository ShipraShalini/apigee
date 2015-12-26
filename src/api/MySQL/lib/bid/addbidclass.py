from src.common.helpers.getrequest import read_request_item
from django.contrib.auth.decorators import login_required
from src.common.models.models import *
from src.api.MySQL.helpers.commonhelper import is_sold, notify


@login_required(login_url='http://localhost:8000/login_message/')
def add_bid(request):
    bidder, item_name, amount = read_request_item(request)
    item = Items.objects.get(item_name = item_name)
    if is_sold(item):
        return ("Cannot Bid: {0}. Item already sold".format(item_name))
    else:
        try:
            bid = bids.objects.get(item = item, bidder = bidder )
        except bids.DoesNotExist:
            bid = bids.objects.create(bidder = bidder, item = item, bid_amount= amount)
            bid_action="Created"
        else:
            bid.bid_amount = amount
            bid.save(update_fields=['bid_amount'])
            bid_action="Modified"

        #function for notifying bidders
        notify(item= item_name, username= bidder, bid_amount= amount)

        return ("{0} Bid: {1} {2}".format(bid_action,bid.item.item_name, bid.bid_amount))
