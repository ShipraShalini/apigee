from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from src.common.helpers.getrequest import read_request_item
from src.common.models.models import Items
from src.common.libraries.scheduler import s
from src.api.MySQL.lib.item.sellitemclass import sell_items



NO_OF_HOURS = 1

@login_required(login_url='http://localhost:8000/login_message/')
def add_items(request):
    seller, item_name, min_bid = read_request_item(request)
    item= Items.objects.create(item_name = item_name, seller = seller, date_added = datetime.now(), min_bid = min_bid )
    exec_time = s.create_exec_time(hour =NO_OF_HOURS)
    s.addjob(function=sell_items, time= exec_time, arguments=[request, item])
    return HttpResponse("Added Item: {0}".format(item.item_name), status= 200)