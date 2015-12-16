from apscheduler.scheduler import Scheduler
from apscheduler.scheduler import Scheduler
from items.models import Items, bids
from django.http import HttpResponse


def sell_items(request):
    item_name = request.REQUEST['name']
    selling_price = request.POST['amount']
    item = Items.objects.get(name = item_name)
    item.status = "Sold"
    item.save()
    return HttpResponse("Item Sold: {} at {}".format(item.name, selling_price), status= 200)

def schedule_sell(exec_time, ):
    sched = Scheduler()
    sched.start()
    job = sched.add_date_job(sell_items, exec_time, ['text'])
    sched.shutdown()



