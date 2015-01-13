from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import re
import json
from datetime import timedelta
import time
import datetime
import socket

UPTIME_VALUES = []
ALERT = False

# Create your views here.
def index(request):
	global UPTIME_VALUES
	global ALERT
	del UPTIME_VALUES[:]
	ALERT = False
	stats = parse_uptime()
	uptime = stats["uptime"]
	users = stats["users"]
	time = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
	ip = socket.gethostbyname(socket.gethostname())
	return render(request, 'load_charts/index.html', locals())

def charts_get(request):
	global UPTIME_VALUES
	time_interval = datetime.datetime.now() - timedelta(minutes=10)
	for pos, val in enumerate(UPTIME_VALUES):
		if time_interval > val["date"] or pos > 60:
			UPTIME_VALUES.pop(pos)
	UPTIME_VALUES.insert(0,curr_load())
	return HttpResponse(convert_json(UPTIME_VALUES))


def check_alerts(request):
	global ALERT
	oldest_record = UPTIME_VALUES[-1]["date"]
	time_interval = datetime.datetime.now() - timedelta(minutes=2)
	data = {}
	data["alert"] = -1
	if time_interval > oldest_record:
		threshold = float(request.GET.get('threshold', ''))
		sum_avg = 0
		nb = 0
		data["time"] = datetime.datetime.now().strftime("%H:%M:%S")
		for pos, val in enumerate(UPTIME_VALUES):
			if val["date"] > time_interval:
				sum_avg += val["value"]
				nb += 1
		if nb:
			avg = sum_avg / nb
			data["value"] = avg
			if avg > threshold:
				if not ALERT:
					ALERT = True
					data["alert"] = 1
			elif ALERT and avg < threshold:
				ALERT=False
				data["alert"] = 0
	return HttpResponse(json.dumps(data))

def convert_json(values):
	temp_values = []
	for val in UPTIME_VALUES:
		temp_values.append(entry(val["date"].strftime("%Y-%m-%d %H:%M:%S"),val["value"]))
	return json.dumps(temp_values)

def curr_load():
	load = parse_uptime()["load"]
	return entry(datetime.datetime.now(), float(load))

def parse_uptime():
	r = subprocess.check_output(["uptime"])
	parsed_dict = {}
	uptime_values = re.split(", ", r)
	load_averages = re.split("load averages: ", uptime_values[3])
	parsed_dict["load"] = re.split(" ",load_averages[1])[0].replace(',', '.')
	parsed_dict["users"] = uptime_values[2]
	parsed_dict["uptime"] = re.split("up ", uptime_values[0])[1]
	return parsed_dict

def entry(date, value):
	new_entry = {}
	new_entry["date"] = date
	new_entry["value"] = value
	return new_entry
