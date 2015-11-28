__author__ = 'hypatia'

from django.core.mail import send_mass_mail
from items.models import Items, bids
from django.contrib.auth.models import User


def getuser(request):
    if request.user.is_authenticated():
        username = request.user.get_username()
        return username

def notify(item, username, bid_amount):
    bid_list = bids.objects.filter(item = item)
    subscribers = []

    for bidder in bid_list:
        User = User.objects.filter(username=bidder.bidder)
        subscribers.append(User.email)

    subject ="New bid on {}".format(item)
    content= "{} bid amount {} on the item {}".format(username, bid_amount, item)
    message=(subject, content, 'from@example.com', subscribers) #create constant list
    send_mass_mail(message)