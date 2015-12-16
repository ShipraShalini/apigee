from django.http import HttpResponse
from items.models import Items, bids
from items.view_helper import Highestbid, is_sold


'''
{
'item_name': 'abc',
}
'''

def view_items(request):
    item_name=request.REQUEST['item_name']
    item = Items.objects.get(name = item_name)
    if is_sold(item):
        return HttpResponse("Item Listed: {} \\n DateCreated: {} \\n Status: {}".format(item.name,
                                                                                        item.date_added,
                                                                                        item.status),
                            status= 200)

    else:
        top_bids = Highestbid(number_of_bids=5, item_name=item_name)

        response= "{1} \\n DateCreated: {2} \\n The top 5 bids:{3}".format(item.name,
                                                                     item.date_added,
                                                                       top_bids)

        return HttpResponse(response, status= 200)