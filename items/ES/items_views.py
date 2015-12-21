
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from view_helper import read_request_item, scheduler, is_sold, Highestbid, values, messages, is_owner
from elastic import add_item, get_item
from es_models import Items,Bids
from elasticsearch_dsl.connections import connections


connections.create_connection(hosts=['localhost'])
s = scheduler()
item =Items.init()


@login_required(login_url='http://localhost:8000/login_message/')
def add_items(request):
    seller, item_name, min_bid =read_request_item(request)
    print seller, item_name, min_bid
    item = add_item(seller, item_name, min_bid)
    exec_time= datetime.now() + timedelta(minutes = 1)
    s.addjob(function=sell_items, time= exec_time, arguments=[item])
    return ("Added Item: {0} {1}".format(item.item_name, item))


#Is payement logic required?
def sell_items(request):
    seller, item_name = read_request_item(request)
    item = Items.get(id = item_name)
    s = Bids.search()
    bid = s.filter("term", item=item_name).execute()
    for b in bid:
        print b.item, b.bidder, b.bid_amount
    a= s.aggs.bucket('SP', 'terms', item=item_name).metric('max_bid', 'max', field='bid_amount')

    res = a.execute()
    # selling_price = s.aggs.filter("term", item=item_name).metric('max_bid', 'max', field='bid_amount')
    #buyer = s.filter("terms", bid_amount = selling_price).execute().bidder
    #print buyer.hits.total, selling_price
    print res.aggregations.max_bid

    if item:
        print "Sold"
        # item.status = "Sold"
        # item.save()
    print("Item Sold: {0} at {1} to {2}".format(item.item_name, selling_price, buyer))


def update_items(request):
    user, item_name, doc = read_request_item(request)
    item = is_owner(item= item_name , user= user)
    if item:
        for k,v in doc.iteritems:
            item[k] = v
        item.save()
        message = messages['ITEM_UPDATED_MESSAGE']
    else:
        message = messages['UNAUTHORISED_ACTION_MESSAGE']
    return message



@login_required(login_url='http://localhost:8000/login_message/')
def del_items(request):
    user, item_name = read_request_item(request)
    item = is_owner(item=item_name, user=user)
    if item:
        item.delete()
        message = "Item {0} deleted".format(item_name)
    else:
        message= messages['CANNOT_PERFORM_ACTION']
    return message


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
        top_bids= Highestbid(N=NUMBER_OF_TOP_BIDS, item=item)
        message = message + "\nThe top {0} bids:\n{1}".format(NUMBER_OF_TOP_BIDS, top_bids)
    return (message)
