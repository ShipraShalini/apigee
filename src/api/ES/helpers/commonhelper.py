from django.core.mail import send_mass_mail
from src.common.libraries.notificationhelper import *
from src.api.ES.helpers.bidhelper import get_bid
from src.common.models.ES_models import Items
from src.api.ES.helpers.itemhelper import get_item

def notify(item, username, bid_amount):
    bid_list = get_bid(item_name= item)
    subscribers = createnotificationlist(bid_list)
    message = createmessage(item,username, bid_amount, subscribers)
    send_mass_mail(message)


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