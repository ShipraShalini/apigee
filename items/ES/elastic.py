from datetime import datetime
from elasticsearch import Elasticsearch, NotFoundError
from elasticsearch_dsl import Search
from es_models import Items, Bids
# from view_helper import create_bid_id



es = Elasticsearch()

s = Search(es, index='item', doc_type='item')

INITIAL_ITEM_STATUS = 'Available'


def create_bid_id(bidder, item):
    return (bidder + '_' + item.item_name)


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


def create_bid(item, bidder, bid_amount):
    bid = Bids()
    bid.item = item
    bid.bidder = bidder
    bid.bid_amount = bid_amount
    bid.save()
    return bid

def modify_bid(bid, amount):
    bid.bid_amount = amount
    bid.save()
    return bid

def get_item(item_name):
    try:
        item = Items.get(id =item_name)
    except NotFoundError:
        return False
    else:
        return item



def get_bid(bidder=None, item_name = None, amount=None):
    try:
        s= Bids.search()
        if item_name:
            if bidder:
                bid = s.filter("term", item = item_name).filter("term", bidder = bidder).execute()
            elif amount:
                bid = s.filter("term", item = item_name).filter("term", bid_amount = amount).execute()
            else:
                bid = s.filter("term", item = item_name).execute()
        elif bidder:
            bid = s.filter("term", bidder = bidder).execute()
        else:
            print "ERROR: Item_name and Bidder not present"
            bid = False
    except NotFoundError:
        return False
    else:
        return bid



    


def del_doc(index, type, doc):
    pass
    #find delete_by_query
