from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import re
import json
from datetime import datetime, timedelta
from time import mktime, strftime, strptime, localtime
import time
import ast

UPTIME_VALUES = []

# Create your views here.
def index(request):
	UPTIME_VALUES = []
	time = strftime("%a, %d %b %Y %H:%M:%S", localtime())
	return render(request, 'load_charts/index.html', locals())

def charts_get(request):
	data = update_log()
	return HttpResponse(data)


def update_log():
	time_interval = datetime.now() - timedelta(minutes=10)
	for pos, val in enumerate(UPTIME_VALUES):
		u = datetime.fromtimestamp(mktime(time.strptime(val["date"], "%Y-%m-%d %H:%M:%S")))
		if time_interval > u or pos > 44:
			UPTIME_VALUES.pop(pos)
	UPTIME_VALUES.insert(0,get_uptime_vals())
	return json.dumps(UPTIME_VALUES)

def empty_file(path):
	open(path, 'w').close()

def get_uptime_vals():
	r = subprocess.check_output(["uptime"])
	load_averages = re.split("load averages: ", r)
	load_avg_last_min = re.split(" ",load_averages[1])[0].replace(',', '.')

	new_entry = {}
	new_entry["date"] = strftime("%Y-%m-%d %H:%M:%S", localtime())
	new_entry["value"] = float(load_avg_last_min)

	return new_entry
