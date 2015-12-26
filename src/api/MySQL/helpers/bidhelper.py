from src.common.models.models import bids


def get_bid(item):
    bid_list = bids.objects.filter(item = item)
    return bid_list

def highestbid(N, item):
    topN={}
    i=1
    topN_result = bids.objects.filter(item = item).order_by('-bid_amount')[:N]
    for bid in topN_result:
        topN[i]=({'Bidder':bid.bidder, 'Item':bid.item.item_name, 'Bid Amount': int(bid.bid_amount)}) #int to remove L character from output
        i=i+1
    return topN