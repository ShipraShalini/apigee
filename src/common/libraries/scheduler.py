import logging
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

class scheduler(object):
    def __init__(self):
        logging.basicConfig()
        self.sched = BackgroundScheduler()
        self.sched.start()

    def create_exec_time(self, hour):
        exec_time= datetime.now() + timedelta(hours = hour)

    def addjob(self, function, time, arguments):
        self.sched.add_job(function, 'date', run_date=time, args= arguments)


s = scheduler()

