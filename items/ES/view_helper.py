__author__ = 'hypatia'

from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from apscheduler.schedulers.background import BackgroundScheduler
import json, logging
from django.http import HttpResponse
from elastic import get_bid, get_item
from es_models import Items, Bids

class scheduler(object):
    def __init__(self):
        logging.basicConfig()
        self.sched = BackgroundScheduler()
        self.sched.start()

    def addjob(self, function, time, arguments):
        print "in addjob"
        self.sched.add_job(function, 'date', run_date=time, args= arguments)

def notify(item, username, bid_amount):
    subscribers = []
    bid_list = get_bid(item_name= item)

    for bidder in bid_list:
        users = User.objects.filter(username__exact=bidder.bidder)
        for user in users:
            subscribers.append(user.email)

    subject = "New bid on {}".format(item)
    content = "{} bid amount {} on the item {}".format(username, bid_amount, item)
    message = (subject, content, 'from@example.com', subscribers) #create constant list
    print message
    #send_mass_mail(message)


def Highestbid(N, item):
    topN={}
    i=1
    s = Bids.search().sort('-bid_amount')
    topN_result = s.filter("term", item = item.item_name).execute()[:N]
    for bid in topN_result:
        topN[i]=({'Bidder':bid.bidder, 'Item':bid.item, 'Bid Amount': int(bid.bid_amount)}) #int to remove L character from output
        i=i+1
    return topN



def values(item):
    return item.item_name, item.created_at, item.status, item.seller, item.min_bid, item.sold_to


def read_request_item(request):
    user = request.user.get_username()

    if request.method == "POST" or request.method == "DELETE" :
        data = json.loads(request.body)
        item_name = data['item']
        try:
            amount = data['amount']
        except KeyError:
            return user, item_name
        else:
            return user, item_name, amount

    if request.method == "GET":
        item_name = request.GET.get('item', None)
        return user, item_name

    if request.method == "PUT":
        data = json.loads(request.body)
        item_name = data['item']
        data = data.pop("item", None)
        return user, item_name, data

messages= dict(ITEM_NOT_PRESENT_MESSAGE="This Item is not Present",
               BID_NOT_PRESENT_MESSAGE="The Bid is not Present",
               UNAUTHORISED_ACTION_MESSAGE="You are not authorised to perform this action.",
               SOLD_MESSAGE="This item is already sold.",
               BID_DELETED_MESSAGE="The bid is deleted.",
               ITEM_DELETED_MESSAGE="The Item is deleted.",
               ITEM_UPDATED_MESSAGE="The Item is updated.",
               CANNOT_PERFORM_ACTION="Cannot Perform action. Unauthorised or Not Present",
               NUMBER_OF_TOP_BIDS = 5

               )


def is_sold(item):
    if isinstance(item, unicode):
        item = Items.get(id = item)

    if item.status == "Sold":
        return True
    else:
        return False


def is_owner(item, user):
    if isinstance(item, unicode):
        item = get_item(item)
    seller = item.seller
    if seller == user:
        return item
    else:
        return False

