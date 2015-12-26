from django.contrib.auth.models import User


def createnotificationlist(bid_list):
    subscribers = []

    for bidder in bid_list:
        users = User.objects.filter(username__exact=bidder.bidder)
        for user in users:
            subscribers.append(user.email)

    return subscribers


def createmessage(item,username, bid_amount, subscribers):
    subject = "New bid on {}".format(item.item_name)
    content = "{} bid amount {} on the item {}".format(username, bid_amount, item)
    message = (subject, content, 'root@shipra.ninja', subscribers) #create constant list
    return message