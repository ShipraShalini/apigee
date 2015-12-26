from django.core.mail import send_mass_mail
from src.common.libraries.notificationhelper import *
from src.api.MySQL.helpers.bidhelper import get_bid

def notify(item, username, bid_amount):
    bid_list = get_bid(item= item)
    subscribers = createnotificationlist(bid_list)
    message = createmessage(item,username, bid_amount, subscribers)
    send_mass_mail(message)


def is_sold(item):
    if item.status == "Sold":
        return True
    else:
        return False