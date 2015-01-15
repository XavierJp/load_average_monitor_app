from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import re
import json
from datetime import timedelta
import time
import datetime
import socket
import ast


# Create your views here.
def index(request):
	"""
		index view function
    """
	return render(request, 'load_charts/index.html', locals())

def get_charts_values(request):
	"""
		On AJAX call, returns updated data values to populate new chart.
		returns content of ./load_charts/static/load_charts/uptime_log, updated by a cron task
	"""
	log_file = open('./load_charts/static/load_charts/uptime_log', 'r')
	uptime_values = ast.literal_eval(log_file.read())
	log_file.close()
	return HttpResponse(json.dumps(uptime_values))

def get_updated_date(request):
	"""
		On AJAX call, returns updated data values to populate new chart
	"""
	# read current values in chart
	log_file = open('./load_charts/static/load_charts/uptime_log', 'r')
	uptime_values = ast.literal_eval(log_file.read())
	log_file.close()
	#defines current oldest entry
	oldest_record = datetime.datetime.strptime(uptime_values[-1]["date"], '%Y-%m-%d %H:%M:%S')
	#defines a two minutes interval from now
	time_interval = datetime.datetime.utcnow() - timedelta(minutes=2)

	# creates a dict with stats from uptime statistics (uptime, users ...)
	data = parse_uptime()
	# default alert is -1 nothing is triggered
	data["alert"] = -1

	# we need at least a two minutes history
	if time_interval > oldest_record:
		threshold = float(request.GET.get('threshold', ''))
		sum_avg = 0
		nb = 0
		# compute avg load on past two minutes
		for pos, val in enumerate(uptime_values):
			val_date = datetime.datetime.strptime(val["date"], '%Y-%m-%d %H:%M:%S')
			if val_date > time_interval:
				sum_avg += val["value"]
				nb += 1
		# Case avg > threshold set alert to 1 else set alert to 0
		if nb:
			avg = sum_avg / nb
			data["value"] = avg
			if avg > threshold:
				data["alert"] = 1
			elif avg < threshold:
				data["alert"] = 0

	return HttpResponse(json.dumps(data))

def parse_uptime():
	"""
		Returns a dict containing result of parse of uptime in console
	"""
	r = subprocess.check_output(["uptime"])
	parsed_dict = {}

	#load average over past minute

	# code for linux
	uptime_values = re.split(", ", r)
	load_averages = re.split("load average: ", uptime_values[3])
	parsed_dict["load"] = re.split(", ",load_averages[1])[0]
	
	# code for Unix (Mac)
	# uptime_values = re.split(", ", r)
	# load_averages = re.split("load averages: ", uptime_values[3])
	# parsed_dict["load"] = re.split(" ",load_averages[1])[0].replace(',', '.')

	parsed_dict["users"] = uptime_values[2]
	parsed_dict["uptime"] = re.split("up ", uptime_values[0])[1]
	# US formated datetime to be displayed in top right corner
	parsed_dict["date"] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	# Server IP Adress
	parsed_dict["ip"] = socket.gethostbyname(socket.gethostname())
	# Time to be displayed in alert container

	return parsed_dict

