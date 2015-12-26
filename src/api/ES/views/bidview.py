from django.http import HttpResponse
from src.api.ES.lib.bid.addbidclass import add_bid
from src.api.ES.lib.bid.deletebidclass import del_bids
from src.api.ES.lib.bid.viewbidclass import view_bids

def bid(request):
    if request.method == "GET":
        message = view_bids(request)

    elif request.method == "POST":
        message= add_bid(request)

    elif request.method == "DELETE":
        message = del_bids(request)

    else:
        message = "Only GET/PUT/POST allowed"

    return HttpResponse(message)
