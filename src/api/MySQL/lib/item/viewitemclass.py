from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from src.common.helpers.getrequest import read_request_item
from src.common.models.models import Items
from src.api.MySQL.helpers.bidhelper import highestbid
from src.api.MySQL.helpers.commonhelper import is_sold



@login_required(login_url='http://localhost:8000/login_message/')
def view_items(request):
    seller, item_name = read_request_item(request)
    item = Items.objects.get(item_name = item_name)
    date = item.date_added.strftime("%A, %B %d %Y, %H:%M:%S")
    message= "Item Listed: {0} \\n DateCreated: {1} \\n Status: {2}".format(item.name, date, item.status)
    if is_sold(item):
        return HttpResponse(message, status= 200)
    else:
        top_bids= highestbid(N=5, item=item)
        return HttpResponse(message + "The top 5 bids:\n{2}".format(item.item_name, date, top_bids), status= 200)