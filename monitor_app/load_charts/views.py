from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import re
import json
from datetime import timedelta
from time import mktime, strftime, strptime, localtime
import time
import datetime
import ast

UPTIME_VALUES = []
ALERT = False

# Create your views here.
def index(request):
	global UPTIME_VALUES
	del UPTIME_VALUES[:]
	ALERT = False
	time = strftime("%a, %d %b %Y %H:%M:%S", localtime())
	return render(request, 'load_charts/index.html', locals())

def charts_get(request):
	global UPTIME_VALUES
	time_interval = datetime.datetime.now() - timedelta(minutes=10)
	for pos, val in enumerate(UPTIME_VALUES):
		val_date = datetime.datetime.strptime(val["date"], "%Y-%m-%d %H:%M:%S")
		if time_interval > val_date or pos > 60:
			UPTIME_VALUES.pop(pos)
	UPTIME_VALUES.insert(0,get_uptime_vals())
	data = json.dumps(UPTIME_VALUES)
	return HttpResponse(data)

def check_alerts(request):
	global ALERT
	threshold = float(request.GET.get('threshold', ''))
	time_interval = datetime.datetime.now() - timedelta(minutes=2)
	sum_avg = 0
	data = -1
	nb = 0
	for pos, val in enumerate(UPTIME_VALUES):
		val_date = datetime.datetime.strptime(val["date"], "%Y-%m-%d %H:%M:%S")
		if val_date > time_interval:
			sum_avg += val["value"]
			nb += 1
	if nb:
		avg = sum_avg / nb
		if avg > threshold:
			if not ALERT:
				ALERT = True
				data = 1
			if ALERT:
				data = -1
		elif ALERT and avg < threshold:
			ALERT=False
			data = 0
	return HttpResponse(data)

def get_uptime_vals():
	r = subprocess.check_output(["uptime"])
	load_averages = re.split("load averages: ", r)
	load_avg_last_min = re.split(" ",load_averages[1])[0].replace(',', '.')
	new_entry = {}
	new_entry["date"] = strftime("%Y-%m-%d %H:%M:%S", localtime())
	new_entry["value"] = float(load_avg_last_min)
	return new_entry
