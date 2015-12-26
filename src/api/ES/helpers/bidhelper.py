from elasticsearch import NotFoundError
from src.common.models.ES_models import Bids


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


def highestbid(N, item):
    topN={}
    i=1
    s = Bids.search().sort('-bid_amount')
    topN_result = s.filter("term", item = item.item_name).execute()[:N]
    for bid in topN_result:
        topN[i]=({'Bidder':bid.bidder, 'Item':bid.item, 'Bid Amount': int(bid.bid_amount)}) #int to remove L character from output
        i=i+1
    return topN
