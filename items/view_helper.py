__author__ = 'hypatia'

from django.core.mail import send_mass_mail
from items.models import bids
from django.contrib.auth.models import User
from items.models import Items

def notify(item, username, bid_amount):
    bid_list = bids.objects.filter(item = item)
    subscribers = []

    for bidder in bid_list:
        users = User.objects.filter(username=bidder.bidder)
        for user in users:
            subscribers.append(user.email)

    subject ="New bid on {}".format(item)
    content= "{} bid amount {} on the item {}".format(username, bid_amount, item)
    message=(subject, content, 'from@example.com', subscribers) #create constant list
    print message
    #send_mass_mail(message)

def Highestbid(number_of_bids, item_name ):
    top_bids=[]
    top_result = bids.objects.filter(item = item_name).order_by('-bid_amount')[:number_of_bids]
    for bid in top_result:
        top_bids.append({'Bidder':bid.bidder, 'Item':bid.item.name, 'Bid Amount': bid.bid_amount})
    return top_bids

def is_sold(item):
    if item.status == "Sold":
        return True
    else:
        return False


def pub_ip():
    #ip addr show eth0 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'
    #uwsgi --http :8080 --home /home/user/Env/firstsite --chdir /home/user/firstsite -w firstsite.wsgi
    pass
