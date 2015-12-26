from django.contrib.auth.decorators import login_required
from src.common.helpers.getrequest import read_request_item
from items.ES.constants import messages
from src.api.ES.helpers.commonhelper import is_owner


@login_required(login_url='http://localhost:8000/login_message/')
def del_items(request):
    user, item_name = read_request_item(request)
    item = is_owner(item=item_name, user=user)
    if item:
        item.delete()
        message = "Item {0} deleted".format(item_name)
    else:
        message= messages['CANNOT_PERFORM_ACTION']
    return message

