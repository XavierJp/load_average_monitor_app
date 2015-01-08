from django.shortcuts import render
from django.http import HttpResponse
import subprocess

# Create your views here.
def index(request):
	r = subprocess.check_output(["uptime"])
	return render(request, 'load_charts/index.html', locals())