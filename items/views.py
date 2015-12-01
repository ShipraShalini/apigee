from django.http import HttpResponse
from datetime import datetime, time
from items.models import Items, bids
from notification import notify



def add_items(request):
    seller = request.user
    if seller:
        if request.method == "POST": #find way to pass null to image_url
            item= Items.objects.create(name = request.POST['name'],
                                       seller = seller,
                                       date_added = datetime.now(),
                                        min_bid = request.POST['min_bid'] )
            return HttpResponse("Added Item: {}".format(item.name), status= 200)

    else:
        return HttpResponse("Please log in") #redirect to login


def del_items(request):
    item_name=request.REQUEST['name']
    Items.objects.get(name = item_name).delete()
    return HttpResponse("Item deleted {}".format(item_name), status= 200)


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
    #input item, amount
    bidder = request.user
    if bidder:
        if request.method == "POST":
            item_name = request.POST['item']
            item = Items.objects.get(name = item_name)
            if item.status == 'Sold':
                return HttpResponse("Cannot Bid: {}. Item already sold".format(item_name), status= 200)

            else:
                bid_amount= request.POST['amount']

                try:
                    bid = bids.objects.get(item = item, bidder = bidder )

                except bids.DoesNotExist:
                    bid = bids.objects.create(bidder = bidder,
                                            item = item,
                                            bid_amount= bid_amount)
                else:
                    bid.bid_amount = bid_amount
                    bid.save()
                    print"edited"

                #function for notifying bidders
                notify(item= item_name, username= bidder, bid_amount= bid_amount)

                return HttpResponse("Added Bid: {} {}".format(bid.item, bid.bid_amount), status= 200)
    else:
        return HttpResponse("Please log in")


def del_bids(request):
    bidder = request.user
    if bidder:
        item_name=request.REQUEST['item']
        try:
            bids.objects.get(item__exact = item_name,bidder__exact = bidder).delete()
        except:
            return HttpResponse("Error: could not delete item {}. Retry".format(item_name))
        else:
            return HttpResponse("OK 200 Bid deleted {} for ".format(item_name), status= 200)
    else:
        return HttpResponse("Please log in")


#is it needed
def view_bids(request):
    bidder = request.user
    if bidder:
        bid_list = bids.objects.filter(bidder = bidder)
        for bid in bid_list:
            print "print bid:" ,bid.item.name, bid.bidder, bid.bid_amount
        return HttpResponse("Bids Listed: {}".format(bid_list), status= 200)
    else:
        return HttpResponse("Please log in")

