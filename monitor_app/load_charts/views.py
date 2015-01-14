from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import re
import json
from datetime import timedelta
import time
import datetime
import socket
import threading
import ast


# Create your views here.
def index(request):
	return render(request, 'load_charts/index.html', locals())

def get_charts_values(request):
	log_file = open('./load_charts/static/load_charts/uptime_log', 'r')
	uptime_values = ast.literal_eval(log_file.read())
	log_file.close()
	return HttpResponse(json.dumps(uptime_values))

def get_updated_date(request):

	log_file = open('./load_charts/static/load_charts/uptime_log', 'r')
	uptime_values = ast.literal_eval(log_file.read())
	log_file.close()

	oldest_record = datetime.datetime.strptime(uptime_values[-1]["date"], '%Y-%m-%d %H:%M:%S')
	time_interval = datetime.datetime.now() - timedelta(minutes=2)

	data = parse_uptime()
	data["alert"] = -1
	if time_interval > oldest_record:
		threshold = float(request.GET.get('threshold', ''))
		sum_avg = 0
		nb = 0
		data["time"] = datetime.datetime.now().strftime("%H:%M:%S")
		for pos, val in enumerate(uptime_values):
			val_date = datetime.datetime.strptime(val["date"], '%Y-%m-%d %H:%M:%S')
			if val_date > time_interval:
				sum_avg += val["value"]
				nb += 1
		if nb:
			avg = sum_avg / nb
			data["value"] = avg
			if avg > threshold:
				data["alert"] = 1
			elif avg < threshold:
				data["alert"] = 0
	return HttpResponse(json.dumps(data))

def curr_load():
	r = subprocess.check_output(["uptime"])
	load = re.split("load averages: ", r)[0].replace(',', '.')
	return entry(datetime.datetime.now(), float(load))

def parse_uptime():
	r = subprocess.check_output(["uptime"])
	parsed_dict = {}
	uptime_values = re.split(", ", r)
	load_averages = re.split("load averages: ", uptime_values[3])
	parsed_dict["load"] = re.split(" ",load_averages[1])[0].replace(',', '.')
	parsed_dict["users"] = uptime_values[2]
	parsed_dict["uptime"] = re.split("up ", uptime_values[0])[1]
	parsed_dict["clock"] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
	parsed_dict["ip"] = socket.gethostbyname(socket.gethostname())
	return parsed_dict

def entry(date, value):
	new_entry = {}
	new_entry["date"] = date
	new_entry["value"] = value
	return new_entry
