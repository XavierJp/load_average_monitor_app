from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import re
import json

# Create your views here.
def index(request):
	raw_file=open('./load_charts/static/load_charts/uptime_log', 'w')
	raw_file.write('')
	raw_file.close
	return render(request, 'load_charts/index.html', locals())

def test_get(request):
	data = update_log()
	return HttpResponse(data)


def update_log():
	r = subprocess.check_output(["uptime"])
	hour = r[:5]
	load_averages = re.split("load averages: ", r)
	load_avg_last_min = re.split(" ",load_averages[1])[0]

	raw_file=open('./load_charts/static/load_charts/uptime_log', 'a+')


	string_to_add = ',{"hour":"'+hour+'","value":'+load_avg_last_min.replace(',', '.')+'}\n'

	raw_file.write(string_to_add)
	raw_file.seek(0)
	data = "["+raw_file.read()[1:]+"]"
	raw_file.close
	return data