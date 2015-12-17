from items_views import add_items, view_items, del_items

def item(request):
    if request.method == "GET":
        view_items(request)

    if request.method == "POST":
        add_items(request)

    if request.method == "DELETE":
        del_items(request)
