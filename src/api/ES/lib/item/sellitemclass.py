from src.common.models.ES_models import Bids
from src.api.ES.helpers.itemhelper import update_item
from src.api.ES.helpers.bidhelper import get_bid

ITEM_INDEX= 'item'


def sell_items(item):
    s = Bids.search()
    s.aggs.bucket('SP', 'terms', field=ITEM_INDEX).metric('max_bid', 'max', field='bid_amount')
    response = s.execute()

    for term in response.aggregations.SP.buckets:
        if term.key == item.item_name:
            selling_price = term.max_bid.value

    buyer = get_bid(item_name=item.item_name, amount=selling_price)[0].bidder
    doc = dict(status="Sold", sold_to=buyer)
    update_item(item= item, key_value=doc)

    return "Item Sold: {0} at {1} to {2}".format(item.item_name, selling_price, buyer)