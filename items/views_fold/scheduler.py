from apscheduler.scheduler import Scheduler
from datetime import datetime, timedelta



sched = Scheduler()
sched.start()
sched.daemonic = False

def print_in(text):
    print text

xyz=123
exec_time1= datetime.now() + timedelta(seconds=4)
exec_time2= datetime.now() + timedelta(seconds=2)
job1 = sched.add_date_job(print_in, exec_time1, [xyz])
job2 = sched.add_date_job(print_in, exec_time2, ['abc'])


#sched.shutdown()