from src.common.helpers.getrequest import read_request_item
from django.contrib.auth.decorators import login_required
from src.common.models.models import bids
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

    return "User: {0} \nBids: \n{1}".format(bidder, bid_dict)