from bid_views import add_bid, view_bids, del_bids
from django.http import HttpResponse

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
