__author__ = 'hypatia'

from django.core.mail import send_mass_mail
from items.models import bids
from django.contrib.auth.models import User

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