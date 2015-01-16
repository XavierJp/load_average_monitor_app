from django.test import TestCase
import random
from django.views import get_updated_date


class AlertLogicTest(TestCase):

    def setUp(self):
    	self.threshold = 1.0
        self.uptime_log_str_alert = self.generate_uptime_log(True)
        self.uptime_log_str_correct = self.generate_uptime_log(False)

    def test_alert(self):
        self.assertEqual(self.threshold, 1.0)

    def generate_uptime_log(self, bool):
    	now = datetime.datetime.utcnow()
    	date = now - timedelta(minutes=10)
    	list_of_values = []
        while date < now:
            entry = {}
            entry["date"] = date
            if bool:
            	entry["value"] = threshold - float(randint(1, 40))/10
			else:
            	entry["value"] = threshold + float(randint(1, 40))/100
        	list_of_values.append(entry)
        	date = date + timedelta(seconds=10)
        return str(list_of_values)