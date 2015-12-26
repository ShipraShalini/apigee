from django.contrib.auth.decorators import login_required
from src.api.ES.helpers.itemhelper import get_item
from src.api.ES.helpers.bidhelper import highestbid
from src.common.helpers.getrequest import read_request_item, values
from src.api.ES.helpers.commonhelper import is_sold
from items.ES.constants import messages



@login_required(login_url='http://localhost:8000/login_message/')
def view_items(request):
    seller, item_name = read_request_item(request)
    item = get_item(item_name)
    if item:
        item_name, created_at, status, seller, min_bid, sold_to =values(item)
        message= "Item Listed: {0} \nDateCreated: {1} \nStatus: {2} \nSeller : {3} \nMinimum Bid: {4} \nSold To: {5}".format(item_name, created_at, status, seller, min_bid, sold_to)
    else:
        return messages['ITEM_NOT_PRESENT_MESSAGE']

    if is_sold(item):
        return (message)
    else:
        NUMBER_OF_TOP_BIDS= messages['NUMBER_OF_TOP_BIDS']
        top_bids= highestbid(N=NUMBER_OF_TOP_BIDS, item=item)
        message = message + "\nThe top {0} bids:\n{1}".format(NUMBER_OF_TOP_BIDS, top_bids)
    return (message)
