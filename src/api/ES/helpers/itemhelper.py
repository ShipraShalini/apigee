
from datetime import datetime
from elasticsearch import NotFoundError
from src.common.models.ES_models import Items


INITIAL_ITEM_STATUS = 'Available'


def add_item(seller, item_name, min_bid):
    item = Items(meta={'id': item_name})
    item.item_name = item_name
    item.status = INITIAL_ITEM_STATUS
    item.seller = seller
    # item.created_at = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    item.min_bid = min_bid
    item.sold_to = None
    item.save()
    return item


def get_item(item_name):
    try:
        item = Items.get(id =item_name)
    except NotFoundError:
        return False
    else:
        return item


def update_item(item, key_value):
    for k,v in key_value.iteritems():
        item[k] = v
        item.save()
    return item




