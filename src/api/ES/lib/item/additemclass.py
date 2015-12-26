from django.contrib.auth.decorators import login_required
from src.common.libraries.scheduler import s
from src.api.ES.helpers.itemhelper import get_item
from src.api.ES.lib.item.sellitemclass import sell_items
from src.common.helpers.getrequest import read_request_item


NO_OF_HOURS= 1

@login_required(login_url='http://localhost:8000/login_message/')
def add_items(request):
    seller, item_name, min_bid =read_request_item(request)
    item = get_item(item_name=item_name)
    exec_time = s.create_exec_time(NO_OF_HOURS)
    s.addjob(function=sell_items, time= exec_time, arguments=[request, item])
    return ("Added Item: {0} {1}".format(item.item_name, item.__dict__))