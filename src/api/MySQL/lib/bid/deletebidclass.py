from src.common.helpers.getrequest import read_request_item
from django.contrib.auth.decorators import login_required
from src.common.models.models import bids

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
        return "Bid deleted for {0} ".format(item_name)