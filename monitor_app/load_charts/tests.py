from django.core.urlresolvers import resolve
from django.test import TestCase
from load_charts.views import get_updated_stats
from django.http import HttpRequest
import ast
import re


class AlertLogicTest(TestCase):

	def test_get_stats_returns_correct_content(self):
		""" test content returned by GET on /get-stats """

		response = self.create_request('/load_charts/get-stats/', 1.0)

		# test every keys
		for k in ['load', 'alert', 'value', 'ip', 'users', 'uptime', 'date']:
			self.assertTrue(k in response.keys()) 
		
		# test that alert is either 1 (>> alert level) or 0 (>> no-alert) or -1 (>> not enough value to compute average)
		self.assertTrue(response["alert"] in [1,0,-1])

		# lower threshold to trigger an alert signal
		threshold_alert = round(float(response["value"]))
		response_alert = self.create_request('/load_charts/get-stats/', threshold_alert)
		self.assertTrue(response_alert["alert"] == 1)

		# raise thrshold to trigger a recover signal
		threshold_recover = threshold_alert + 1
		response_recover = self.create_request('/load_charts/get-stats/', threshold_recover)
		self.assertTrue(response_recover["alert"] == 0)


	def test_url_resolves_correct_function(self):
		""" test that correct view function is called """
		found = resolve('/load_charts/get-stats/')
		self.assertEqual(found.func, get_updated_stats)  

	def create_request(self, url, threshold):
		""" creates request call get_updated_stats and parse answer """
		request = HttpRequest() 
		request.path = url
		request.GET = {'threshold': str(threshold)}
		cleaned_response = re.split('Content-Type: text/html; charset=utf-8\r\n\r\n', str(get_updated_stats(request)))[-1]
		return eval(cleaned_response)