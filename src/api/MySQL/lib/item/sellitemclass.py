from src.common.models.models import bids
from django.db.models import Max


#Is payement logic required?
def sell_items(item):
    selling_price = bids.objects.filter(item=item).aggregate(Max('bid_amount'))['bid_amount__max']
    buyer = bids.objects.get(item=item, bid_amount = selling_price).bidder
    item.status = "Sold"
    item.save(update_fields=['status'])
    print("Item Sold: {0} at {1} to {2}".format(item.item_name, selling_price, buyer))
    #return HttpResponse("Item Sold: {0} at {1} to {2}".format(item.item_name, selling_price, buyer), status= 200)