from django.contrib.auth.decorators import login_required
from items.ES.constants import messages
from src.api.ES.helpers.itemhelper import update_item
from src.api.ES.helpers.commonhelper import is_owner
from src.common.helpers.getrequest import read_request_item



@login_required(login_url='http://localhost:8000/login_message/')
def modify_items(request):
    user, item_name, doc = read_request_item(request)
    print "UP", type(doc)
    item = is_owner(item= item_name , user= user)
    if item:
        update_item(item= item, key_value=doc)
        message = messages['ITEM_UPDATED_MESSAGE']
    else:
        message = messages['UNAUTHORISED_ACTION_MESSAGE']
    return message

