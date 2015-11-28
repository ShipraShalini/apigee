from django.http import HttpResponse
from datetime import datetime
from items.models import Items, bids



def add_items(request):
    if request.method == "POST":
        item= Items.objects.create(name = request.POST['name'],
                                    date_added = datetime.now(),
                                    image= request.POST['image_url'])
        return HttpResponse("Added Item: {}".format(item.name), status= 200)


def del_items(request):
    item_name=request.REQUEST['name']
    Items.objects.get(name = item_name).delete()
    return HttpResponse("OK 200 Item deleted {}".format(item_name), status= 200)


def view_items(request):
    item_name=request.REQUEST['name']
    item = Items.objects.get(name = item_name)
    if item.status == "Sold":
        return HttpResponse("Item Listed: {} \\n DateCreated: {} \\n Status: {}".format(item.name,
                                                                                        item.date_added,
                                                                                        item.status),
                            status= 200)

    else:
        #find top 5 bids
        top5=[]
        top5_result = bids.objects.filter(item = item_name).order_by('-bid_amount')[:5]
        for bid in top5_result:
            top5.append({'Bidder':bid.bidder, 'Item':bid.item.name, 'Bid Amount': bid.bid_amount})

        return HttpResponse("OK 200 Item Listed: {} \\n DateCreated: {} \\n The top 5 bids: \\n {}".format(item.name,
                                                                                                           item.date_added,
                                                                                                           top5),
                            status= 200)


#Is payement logic required?
def sell_items(request):
    item_name = request.REQUEST['name']
    selling_price = request.POST['amount']
    item = Items.objects.get(name = item_name)
    item.status = "Sold"
    item.save()
    return HttpResponse("Item Sold: {} at {}".format(item.name, selling_price), status= 200)




def add_bid(request):
    if request.method == "POST":
        item_name = request.POST['item']
        bidder =  request.POST['name']
        bid_amount= request.POST['amount']

        try:
            bid = bids.objects.get(name = item_name, bidder = bidder ),

        except bids.DoesNotExist:
            bid = bids.objects.create(bidder = bidder,  #find out way of retrieving user form login info
                                    item = item_name,
                                    bid_amount= bid_amount)
        else:
            bid.bid_amount = bid_amount
            bid.save()

        #function for notifying bidders
        #
        #
        return HttpResponse("Added Item: {} {}".format(bid.item, bid.bid_amount), status= 200)


def del_bids(request):
    item_name=request.REQUEST['name']
    bidder = request.REQUEST['name']
    bids.objects.get(Q(name__exact = item_name),
                     Q(bidder__exact = bidder  )).delete()
    return HttpResponse("OK 200 Bid deleted {} for ".format(item_name), status= 200)

#is it needed
def view_bids(request):
    bidder=request.REQUEST['name']
    bid_list = bids.objects.filter(name = bidder)
    #create a time left function
    #create function to view to 5

    return HttpResponse("Bids Listed: {}".format(bid_list), status= 200)

