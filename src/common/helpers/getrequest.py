import json

def read_request_item(request):
    user = request.user.get_username()

    if request.method == "POST" or request.method == "DELETE" :
        data = json.loads(request.body)
        item_name = data['item']
        try:
            amount = data['amount']
        except KeyError:
            return user, item_name
        else:
            return user, item_name, amount

    if request.method == "GET":
        item_name = request.GET.get('item', None)
        return user, item_name

    if request.method == "PUT":
        data = json.loads(request.body)
        item_name = data['item']
        del data['item']
        return user, item_name, data


def values(item):
    return item.item_name, item.created_at, item.status, item.seller, item.min_bid, item.sold_to