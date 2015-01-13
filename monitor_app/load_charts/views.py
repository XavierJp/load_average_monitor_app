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
SEUIL = 1.50

# Create your views here.
def index(request):
	del UPTIME_VALUES[:]
	time = strftime("%a, %d %b %Y %H:%M:%S", localtime())
	return render(request, 'load_charts/index.html', locals())

def charts_get(request):
	data = update_log()
	return HttpResponse(data)

def check_alerts(request):
	time_interval = datetime.datetime.now() - timedelta(minutes=2)
	data = ''
	sum_avg = 0
	nb = 0
	for pos, val in enumerate(UPTIME_VALUES):
		val_date = datetime.datetime.strptime("%Y-%m-%d %H:%M:%S", val["date"])
		if val_date > time_interval:
			sum_avg += val["value"]
			nb += 1
	if nb:
		avg = sum_avg / nb
		if avg > SEUIL:
			if not ALERT:
				ALERT = True
				data = "alert"
		else:
			if ALERT:
				ALERT=False
				data = "finalert"
	return HttpResponse(data)


def update_log():
	time_interval = datetime.datetime.now() - timedelta(minutes=10)
	for pos, val in enumerate(UPTIME_VALUES):
		val_date = datetime.datetime.strptime("%Y-%m-%d %H:%M:%S", val["date"])
		if time_interval > val_date or pos > 60:
			UPTIME_VALUES.pop(pos)
	UPTIME_VALUES.insert(0,get_uptime_vals())
	return json.dumps(UPTIME_VALUES)

def get_uptime_vals():
	r = subprocess.check_output(["uptime"])
	load_averages = re.split("load averages: ", r)
	load_avg_last_min = re.split(" ",load_averages[1])[0].replace(',', '.')
	new_entry = {}
	new_entry["date"] = strftime("%Y-%m-%d %H:%M:%S", localtime())
	new_entry["value"] = float(load_avg_last_min)
	return new_entry
