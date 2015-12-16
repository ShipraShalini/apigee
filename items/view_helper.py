__author__ = 'hypatia'

from django.core.mail import send_mass_mail
from items.models import bids
from django.contrib.auth.models import User
from apscheduler.schedulers.background import BackgroundScheduler
import json, logging


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
    bid_list = bids.objects.filter(item = item)

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
    topN_result = bids.objects.filter(item = item).order_by('-bid_amount')[:N]
    for bid in topN_result:
        topN[i]=({'Bidder':bid.bidder, 'Item':bid.item.item_name, 'Bid Amount': int(bid.bid_amount)}) #int to remove L character from output
        i=i+1
    return topN



def is_sold(item):
    if item.status == "Sold":
        return True
    else:
        return False


def pub_ip():
    #ip addr show eth0 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'
    #uwsgi --http :8080 --home /home/users/Env/firstsite --chdir /home/users/firstsite -w firstsite.wsgi
    pass


def read_request_item(request):
    user = request.user
    if request.method == "POST":
        data = json.loads(request.body)
        item_name = data['item']
        try:
            amount = data['amount']
        except KeyError:
            return user, item_name
        else:
            return user, item_name, amount

