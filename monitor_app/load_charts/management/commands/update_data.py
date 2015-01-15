import datetime
import re
import subprocess
from datetime import timedelta
from django.core.management.base import BaseCommand
import time
import ast
import os

file_path = os.path.abspath(os.path.dirname(__file__+"/../../../"))

class Command(BaseCommand):

    help = 'update uptime log dict'

    def handle(self, *args, **options):
        for t in xrange(6):
            self.update_file()
            time.sleep(10)

    def update_file(self):
        log_path = file_path+'/static/load_charts/uptime_log'
        log_file = open(str(log_path), 'r')
        log = log_file.read()
        log_file.close()
        uptime_values = ast.literal_eval(log)
        time_interval = datetime.datetime.now() - timedelta(minutes=10)
        for pos, val in reversed(list(enumerate(uptime_values))):
            val_date = datetime.datetime.strptime(val["date"], '%Y-%m-%d %H:%M:%S')
            if time_interval > val_date:
                uptime_values.pop(pos)
        uptime_values.insert(0,self.curr_load())
        log_file = open(str(log_path), 'w')
        log_file.write(str(uptime_values))
        log_file.close()

    def curr_load(self):
        r = subprocess.check_output(["uptime"])
        load_averages = re.split("load average: ", r)
        load = re.split(", ",load_averages[1])[0]
        return self.entry(datetime.datetime.now(), float(load))

    def entry(self, date, value):
        new_entry = {}
        new_entry["date"] = date.strftime('%Y-%m-%d %H:%M:%S')
        new_entry["value"] = value
        return new_entry