
from src.api.ES.lib.item.additemclass import add_items
from src.api.ES.lib.item.deleteitemclass import del_items
from src.api.ES.lib.item.viewitemclass import view_items
from src.api.ES.lib.item.modifyitemclass import modify_items
from django.http import HttpResponse

def item(request):

    if request.method == "GET":
        message = view_items(request)

    if request.method == "POST":
        message= add_items(request)

    if request.method == "DELETE":
        message = del_items(request)

    if request.method == "PUT":
        message = modify_items(request)

    return HttpResponse(message)