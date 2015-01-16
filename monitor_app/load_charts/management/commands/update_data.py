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

    """
        update uptime log dict
    """

    def handle(self, *args, **options):
        for t in xrange(6):
            self.update_file()
            time.sleep(10)

    def update_file(self):
        """
            populate monitor_app/load_charts/static/load_charts/uptime_log with past ten minutes' load averages 
        """

        log_path = file_path+'/static/load_charts/uptime_log'
        log_file = open(str(log_path), 'r')
        log = log_file.read()
        log_file.close()
        uptime_values = ast.literal_eval(log)
        # defines a ten minutes interval
        time_interval = datetime.datetime.utcnow() - timedelta(minutes=10)
        # enumerates previous entries
        for pos, val in reversed(list(enumerate(uptime_values))):
            val_date = datetime.datetime.strptime(val["date"], '%Y-%m-%d %H:%M:%S')
            # remove them if too old
            if time_interval > val_date:
                uptime_values.pop(pos)
        # insert current load value
        uptime_values.insert(0,self.curr_load())
        # overwrite uptime_log
        log_file = open(str(log_path), 'w')
        log_file.write(str(uptime_values))
        log_file.close()

    def curr_load(self):
        """
            returns a dict with current server load and date
        """
        r = subprocess.check_output(["uptime"])

        # code for linux
        uptime_values = re.split(", ", r)
        load_averages = re.split("load average: ", uptime_values[3])
        load = re.split(", ",load_averages[1])[0]
        
        # code for Unix (Mac)
        # uptime_values = re.split(", ", r)
        # load_averages = re.split("load averages: ", uptime_values[3])
        # load = re.split(" ",load_averages[1])[0].replace(',', '.')
        
        return self.entry(datetime.datetime.utcnow(), float(load))

    def entry(self, date, value):
        """
            builds a dict for curr_load() function
        """
        new_entry = {}
        new_entry["date"] = date.strftime('%Y-%m-%d %H:%M:%S')
        new_entry["value"] = value
        return new_entry