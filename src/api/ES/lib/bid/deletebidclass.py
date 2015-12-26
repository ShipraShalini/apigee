from src.common.helpers.getrequest import read_request_item
from src.api.ES.helpers.bidhelper import get_bid
from items.ES.constants import messages
from django.contrib.auth.decorators import login_required

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
