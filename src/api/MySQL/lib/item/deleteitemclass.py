from django.http import HttpResponse
from src.common.helpers.getrequest import read_request_item
from django.contrib.auth.decorators import login_required
from src.common.models.models import Items


@login_required(login_url='http://localhost:8000/login_message/')
def del_items(request):
    seller, item_name = read_request_item(request)
    try:
        Items.objects.get(item_name = item_name, seller= seller).delete()
    except Items.DoesNotExist:
        return HttpResponse("Item {0} not present".format(item_name), status= 200)
    else:
        return HttpResponse("Item deleted {0}".format(item_name), status= 200)